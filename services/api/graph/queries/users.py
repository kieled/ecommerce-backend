import strawberry
from config import session
from schemas import UserType, HashPasswordType
from services import UserService
from utils import hash_password, IsAdmin, orm_to_strawberry, get_user_ids, IsAuthenticated


@strawberry.type
class UserQuery:
    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Get list of users'
    )
    async def users(self, info, page: int | None = 1) -> list[UserType]:
        async with session() as s:
            data = await UserService(s, info, page=page).list()
            return orm_to_strawberry(data, UserType)

    @strawberry.field(
        permission_classes=[IsAuthenticated],
        description='Get information about current account'
    )
    async def self(self, info) -> UserType:
        temp_user_id, user_id = get_user_ids(info)

        if temp_user_id:
            return UserType(id=0, temp_user_id=temp_user_id)

        async with session() as s:
            data = await UserService(s, info).get(user_id)
            if not data:
                raise Exception('Not found')
            return orm_to_strawberry(data, UserType)

    @strawberry.field(
        description='Get hash for password'
    )
    async def hash(self, password: str) -> HashPasswordType:
        """ Get password hash from string """
        return HashPasswordType(hash=hash_password(password))
