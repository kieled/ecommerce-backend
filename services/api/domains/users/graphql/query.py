import strawberry
from alchemy_graph import orm_to_strawberry

from ..features.location import location_service, LocationType
from ..types import UserType, HashPasswordType
from ..bl import UsersBL
from ..features.auth import hash_password, IsAdmin, get_user_ids, IsAuthenticated


@strawberry.type
class UserQuery:
    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Get list of users'
    )
    async def users(self, info, page: int | None = 1) -> list[UserType]:
        data = await UsersBL(info, page=page).list()
        return orm_to_strawberry(data, UserType)

    @strawberry.field(
        permission_classes=[IsAuthenticated],
        description='Get information about current account'
    )
    async def self(self, info) -> UserType:
        temp_user_id, user_id = get_user_ids(info)

        if temp_user_id:
            return UserType(id=0, temp_user_id=temp_user_id)

        data = await UsersBL(info).get(user_id)
        if not data:
            raise Exception('Not found')
        return orm_to_strawberry(data, UserType)

    @strawberry.field(
        description='Get hash for password'
    )
    async def hash(self, password: str) -> HashPasswordType:
        """ Get password hash from string """
        return HashPasswordType(hash=hash_password(password))

    @strawberry.field(
        description='Get info about location from query'
    )
    async def location_search(self, query: str) -> list[LocationType]:
        return await location_service.search(query)

    @strawberry.field(
        description='Get info about location from lat and lon'
    )
    async def location_reverse(
            self, lat: str, lon: str
    ) -> LocationType:
        return await location_service.reverse(lat, lon)
