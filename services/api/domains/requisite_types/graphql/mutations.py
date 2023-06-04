import strawberry
from strawberry.types import Info

from ..types import RequisiteTypeItemInput, RequisitesTypeItemType, RequisiteTypeCreateInput
from api.utils.graphql import IsAdmin
from ..bl import RequisiteTypeBL


@strawberry.type
class RequisiteTypeMutation:
    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Create requisite type'
    )
    async def create_requisite_type(
            self,
            payload: RequisiteTypeCreateInput,
            info: Info
    ) -> RequisitesTypeItemType:
        data = await RequisiteTypeBL(info).create(payload)
        return RequisitesTypeItemType(**data)

    @strawberry.mutation(permission_classes=[IsAdmin])
    async def update_requisite_type(
            self,
            payload: RequisiteTypeItemInput,
            info: Info
    ) -> None:
        await RequisiteTypeBL(info).update(payload)

    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Delete requisite type'
    )
    async def delete_requisite_type(
            self,
            type_id: int,
            info: Info
    ) -> None:
        await RequisiteTypeBL(info).delete(type_id)
