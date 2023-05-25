from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from alchemy_graph import strawberry_to_dict
from api.schemas import TelegramUserInput
from api.utils import verify_password, get_tokens, assign_response, telegram_hash_check
from .mixins import AppService
from shared.db import User, UserTypeEnum
from api.config import AuthJWT
from shared.base import telegram_config


class UserService(AppService):
    def __init__(self, db: AsyncSession, info, page: int | None = 1):
        self.info = info
        self.request = self.info.context['request']
        self.response = self.info.context['response']
        self.auth = AuthJWT(req=self.request, res=self.response)
        super().__init__(db, User, info, page=page)

    async def get(self, user_id: int) -> User:
        return await self.fetch_one(user_id)

    async def by_username(self, username: str) -> User | None:
        return await self._fetch_first(
            select(User).where(User.username == username)
        )

    async def by_telegram(self, telegram_chat_id: str) -> User | None:
        return await self._fetch_first(
            select(User).where(User.telegram_chat_id == telegram_chat_id)
        )

    async def list(self) -> list[User]:
        return await self.fetch_all()

    async def login(self, username: str, password: str) -> dict:
        """ Login """
        user = await self.by_username(username)

        if not user or not verify_password(password, user.password) or user.type != UserTypeEnum.admin:
            raise Exception('Invalid username/password')

        access, refresh = get_tokens(self.auth, user)
        assign_response(self.auth, access, refresh)
        return dict(
            id=user.id,
            username=user.username
        )

    async def tg_login(self, payload: TelegramUserInput) -> dict:
        """ Telegram auth widget """

        payload_dict = strawberry_to_dict(payload, exclude_none=True)
        if not telegram_hash_check(telegram_config.TG_BOT_TOKEN, payload_dict):
            raise Exception('Invalid hash')
        user = await self.by_telegram(payload.id)

        new_data = dict(
            username=payload.username,
            telegram_chat_id=payload.id,
            first_name=payload.first_name if len(payload.first_name) > 3 else None
        )

        if user:
            sql = update(User).where(User.telegram_chat_id == payload.id).values(
                first_name=new_data.get('first_name')
            )
            await self.db.execute(sql)
        else:
            sql = insert(User).values(**new_data).returning(User.telegram_chat_id)
            user_id = (await self.db.execute(sql)).scalars().first()
            await self.db.commit()
            sql = select(User).where(User.telegram_chat_id == user_id)
            user = (await self.db.execute(sql)).scalars().first()

        access, refresh = get_tokens(self.auth, user)
        assign_response(self.auth, access, refresh)
        return dict(
            username=payload.username,
            first_name=new_data.get('first_name'),
            id=user.id
        )

    async def refresh(self) -> None:
        """ Refresh token """
        try:
            self.auth.jwt_refresh_token_required()
        except Exception as e:
            raise Exception(e.__class__.__name__)
        user_id = self.auth.get_jwt_subject().split(',')[0]
        sql = select(User).options(load_only(User.id, User.type)).where(User.id == int(user_id))
        user = (await self.db.execute(sql)).scalars().first()

        if not user:
            raise Exception('User not found')

        assign_response(self.auth, *get_tokens(self.auth, user))

    def logout(self) -> None:
        self.auth.jwt_required()
        self.auth.unset_jwt_cookies()
