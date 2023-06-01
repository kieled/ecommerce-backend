import strawberry

from api.broker import rabbit_connection
from shared.schemas import MessageSchema
from ..types import UserType, TelegramUserInput, TelegramUserType
from ..bl import UsersBL
from ..features.auth import IsAuthenticated, get_user_ids, AuthJWT


@strawberry.type
class UserMutation:
    @strawberry.mutation(
        description='Administrator authorization'
    )
    async def login(self, username: str, password: str, info) -> UserType:
        """ Login """
        data = await UsersBL(info).login(username, password)
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
        return await UsersBL(info).refresh()

    @strawberry.mutation(
        description='Authorization for customers thought telegram widget'
    )
    async def telegram_login(self, payload: TelegramUserInput, info) -> TelegramUserType:
        """ Login through telegram widget """
        data = await UsersBL(info).tg_login(payload)
        temp_user_id, user_id = get_user_ids(info)
        if temp_user_id:
            await rabbit_connection.send_messages([MessageSchema(
                action='users:migration',
                body={
                    'temp': temp_user_id,
                    'user_id': data.get('id')
                }
            )])
            info.context['response'].delete_cookie('tempId')
        return TelegramUserType(
            username=data.get('username'),
            first_name=data.get('first_name')
        )
