import strawberry
from alchemy_graph import orm_to_strawberry
from strawberry.types import Info
from ..types import RequisitesItemType
from ..bl import RequisiteBL
from api.utils.graphql import IsAdmin


@strawberry.type
class RequisitesQuery:
    @strawberry.field(permission_classes=[IsAdmin])
    async def requisites(
            self,
            type_id: int,
            info: Info
    ) -> list[RequisitesItemType]:
        data = await RequisiteBL(info).list(type_id)
        return orm_to_strawberry(data, RequisitesItemType)

    @strawberry.field
    async def active_requisite(
            self,
            type_id: int,
            info: Info
    ) -> RequisitesItemType:
        data = await RequisiteBL(info).get_active(type_id)
        return orm_to_strawberry(data, RequisitesItemType)
