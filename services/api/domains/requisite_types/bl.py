from alchemy_graph import strawberry_to_dict
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db import RequisiteTypes, cls_session
from .types import RequisiteTypeItemInput, RequisiteTypeCreateInput
from api.domains.mixin import AbstractBL


@cls_session
class RequisiteTypeBL(AbstractBL[RequisiteTypes]):

    async def list(self, session: AsyncSession = None):
        return await self.fetch_all(session)

    async def create(self, payload: RequisiteTypeCreateInput, session: AsyncSession = None):
        payload_dict = strawberry_to_dict(payload)
        return await self.create_item(payload_dict, session)

    async def delete(self, type_id: int, session: AsyncSession = None) -> None:
        await self.delete_item(type_id, session)

    async def update(self, payload: RequisiteTypeItemInput, session: AsyncSession = None) -> None:
        payload_dict = strawberry_to_dict(payload, exclude_none=True, exclude={'id'})
        await self.update_item(
            payload.id,
            payload_dict,
            session
        )
