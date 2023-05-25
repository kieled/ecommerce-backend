import strawberry

from celery_app import migration_task
from config import session, AuthJWT
from schemas import UserType, TelegramUserInput, TelegramUserType
from services import UserService
from utils import IsAuthenticated, get_user_ids


@strawberry.type
class UserMutation:
    @strawberry.mutation(
        description='Administrator authorization'
    )
    async def login(self, username: str, password: str, info) -> UserType:
        """ Login """
        async with session() as s:
            data = await UserService(s, info).login(username, password)
        return UserType(**data)

    @strawberry.mutation(
        permission_classes=[IsAuthenticated],
        description='Logout'
    )
    async def logout(self, info) -> None:
        """ Logout """
        res = info.context["response"]
        req = info.context["request"]

        auth = AuthJWT(req=req, res=res)
        auth.jwt_required()
        auth.unset_jwt_cookies()

    @strawberry.mutation(
        permission_classes=[IsAuthenticated],
        description='Refresh JWT token'
    )
    async def refresh(self, info) -> None:
        """ Refresh token """
        async with session() as s:
            return await UserService(s, info).refresh()

    @strawberry.mutation(
        description='Authorization for customers thought telegram widget'
    )
    async def telegram_login(self, payload: TelegramUserInput, info) -> TelegramUserType:
        """ Login through telegram widget """
        async with session() as s:
            data = await UserService(s, info).tg_login(payload)
        temp_user_id, user_id = get_user_ids(info)
        if temp_user_id:
            migration_task.apply_async(args=[temp_user_id, data.get('id')])
            info.context['response'].delete_cookie('tempId')
        return TelegramUserType(
            username=data.get('username'),
            first_name=data.get('first_name')
        )
