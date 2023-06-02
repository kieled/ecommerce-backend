import strawberry
from strawberry.types import Info
from ..types import RequisitesCreateInput, RequisitesItemType, RequisitesItemInput
from ..bl import RequisiteBL
from api.domains.users.features.auth import IsAdmin


@strawberry.type
class RequisitesMutation:
    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Update transactions info'
    )
    async def update_requisite(
            self,
            payload: RequisitesItemInput,
            info: Info
    ) -> None:
        await RequisiteBL(info).update(payload)

    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Delete requisite'
    )
    async def delete_requisite(
            self,
            requisites_id: int,
            info: Info
    ) -> None:
        await RequisiteBL(info).delete(requisites_id)

    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Create requisite'
    )
    async def create_requisite(
            self,
            payload: RequisitesCreateInput,
            info: Info
    ) -> RequisitesItemType:
        data = await RequisiteBL(info).create(payload)
        return RequisitesItemType(**data)
