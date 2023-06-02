import strawberry
from alchemy_graph import orm_to_strawberry
from strawberry.types import Info

from ..types import RequisitesTypeItemType
from ..bl import RequisiteTypeBL


@strawberry.type
class RequisiteTypeQuery:
    @strawberry.field
    async def requisite_types(
            self,
            info: Info
    ) -> list[RequisitesTypeItemType]:
        data = await RequisiteTypeBL(info).list()
        return orm_to_strawberry(data, RequisitesTypeItemType)
