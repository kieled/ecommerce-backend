import strawberry
from strawberry.types import Info
from config import session
from schemas import RequisitesItemType, RequisitesTypeItemType
from services import RequisitesService, RequisiteTypesService
from utils import IsAdmin, orm_to_strawberry


@strawberry.type
class RequisitesQuery:
    @strawberry.field(permission_classes=[IsAdmin])
    async def requisites(
            self,
            type_id: int,
            info: Info
    ) -> list[RequisitesItemType]:
        async with session() as s:
            data = await RequisitesService(s, info).list(type_id)
        return orm_to_strawberry(data, RequisitesItemType)

    @strawberry.field
    async def active_requisite(
            self,
            type_id: int,
            info: Info
    ) -> RequisitesItemType:
        async with session() as s:
            data = await RequisitesService(s, info).get_active(type_id)
        return orm_to_strawberry(data, RequisitesItemType)

    @strawberry.field
    async def requisite_types(
            self,
            info: Info
    ) -> list[RequisitesTypeItemType]:
        async with session() as s:
            data = await RequisiteTypesService(s, info).list()
        return orm_to_strawberry(data, RequisitesTypeItemType)
