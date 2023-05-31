from alchemy_graph import strawberry_to_dict
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info
from .types import TelegramUserInput
from shared.base import telegram_config
from . import sql
from shared.db import cls_session, User, UserTypeEnum
from .features.auth import verify_password, get_tokens, assign_response, telegram_hash_check
from api.domains.mixin import AbstractBL


@cls_session
class UsersBL(AbstractBL[User]):
    def __init__(self, info: Info, *args, **kwargs):
        super().__init__(User, info, *args, **kwargs)

    async def get(self, user_id: int, session: AsyncSession = None) -> User:
        return await self.fetch_one(user_id, session)

    async def by_username(self, username: str, session: AsyncSession = None) -> User | None:
        filters = (User.username == username,)
        return await self.filter_one(session, filters)

    async def by_telegram(self, telegram_chat_id: str, session: AsyncSession = None) -> User | None:
        filters = (User.telegram_chat_id == telegram_chat_id,)
        return await self.filter_one(session, filters)

    async def list(self, session: AsyncSession = None):
        return await self.fetch_all(session)

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

    async def tg_login(self, payload: TelegramUserInput, session=None) -> dict:
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
            await session.execute(sql.update_first_name(new_data['first_name'], payload.id))
            await session.commit()
        else:
            user_id = (await session.execute(sql.add_new(new_data))).scalars().first()
            await session.commit()
            # TODO: it is probably not working because request get without info selected fields
            user = await self.by_telegram(user_id, session)

        access, refresh = get_tokens(self.auth, user)
        assign_response(self.auth, access, refresh)
        return dict(
            username=payload.username,
            first_name=new_data.get('first_name'),
            id=user.id
        )

    async def refresh(self, session=None) -> None:
        """ Refresh token """
        try:
            self.auth.jwt_refresh_token_required()
        except MissingTokenError:
            return
        user_id = self.auth.get_jwt_subject().split(',')[0]
        user = (await session.execute(
            sql.user_type(int(user_id))
        )).scalars().first()

        assign_response(self.auth, *get_tokens(self.auth, user))

    def logout(self) -> None:
        self.auth.jwt_required()
        self.auth.unset_jwt_cookies()
