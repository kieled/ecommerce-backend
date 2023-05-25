import strawberry
from strawberry.types import Info
from config import session
from schemas import RequisitesCreateInput, RequisitesItemType, RequisitesItemInput, RequisiteTypeCreateInput, \
    RequisitesTypeItemType, RequisiteTypeItemInput
from services import RequisitesService, RequisiteTypesService
from utils import IsAdmin


@strawberry.type
class RequisitesMutation:
    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Update requisites info'
    )
    async def update_requisite(
            self,
            payload: RequisitesItemInput,
            info: Info
    ) -> None:
        async with session() as s:
            await RequisitesService(s, info).update(payload)

    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Delete requisite'
    )
    async def delete_requisite(
            self,
            requisites_id: int,
            info: Info
    ) -> None:
        async with session() as s:
            await RequisitesService(s, info).delete(requisites_id)

    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Create requisite'
    )
    async def create_requisite(
            self,
            payload: RequisitesCreateInput,
            info: Info
    ) -> RequisitesItemType:
        async with session() as s:
            data = await RequisitesService(s, info).create(payload)
        return RequisitesItemType(**data)

    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Create requisite type'
    )
    async def create_requisite_type(
            self,
            payload: RequisiteTypeCreateInput,
            info: Info
    ) -> RequisitesTypeItemType:
        async with session() as s:
            data = await RequisiteTypesService(s, info).create(payload)
        return RequisitesTypeItemType(**data)

    @strawberry.mutation(permission_classes=[IsAdmin])
    async def update_requisite_type(
            self,
            payload: RequisiteTypeItemInput,
            info: Info
    ) -> None:
        async with session() as s:
            await RequisiteTypesService(s, info).update(payload)

    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Delete requisite type'
    )
    async def delete_requisite_type(
            self,
            type_id: int,
            info: Info
    ) -> None:
        async with session() as s:
            await RequisiteTypesService(s, info).delete(type_id)
