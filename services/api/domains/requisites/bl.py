from alchemy_graph import strawberry_to_dict
from sqlalchemy.ext.asyncio import AsyncSession
from shared.db import Requisites, cls_session
from api.domains.mixin import AbstractBL
from .types import RequisitesItemInput, RequisitesCreateInput
from . import sql


@cls_session
class RequisitesBL(AbstractBL[Requisites]):
    def __init__(self, *args, **kwargs):
        super().__init__(Requisites, *args, **kwargs)

    async def list(self, type_id: int, session: AsyncSession):
        filters = (Requisites.type_id == type_id,)
        return await self.fetch_all(session, filters=filters)

    async def get_active(self, type_id: int, session: AsyncSession):
        filters = (
            Requisites.type_id == type_id,
            Requisites.is_active == True
        )
        return await self.filter_one(session, filters)

    async def update(self, payload: RequisitesItemInput, session: AsyncSession) -> None:
        if payload.is_active:
            active_item = (await session.execute(
                sql.active_id(payload.type_id)
            )).scalars().first()
            if active_item:
                await session.execute(
                    sql.deactivate(active_item.id)
                )
        values = strawberry_to_dict(payload, exclude_none=True, exclude={'id', 'type_id'})
        return await self.update_item(payload.id, values, session)

    async def create(self, payload: RequisitesCreateInput, session: AsyncSession):
        items = await self.list(payload.type_id, session)
        is_active = False if len(items) > 0 else False
        payload_dict = strawberry_to_dict(payload)
        payload_dict['is_active'] = is_active
        return await self.create_item(payload_dict, session)

    async def delete(self, requisite_id: int, session: AsyncSession) -> None:
        await self.delete_item(requisite_id, session)