from alchemy_graph import strawberry_to_dict
from sqlalchemy import select, update
from sqlalchemy.orm import load_only
from shared.db import Requisites, cls_session
from api import schemas
from .mixins import AppService


@cls_session
class RequisitesService(AppService):
    def __init__(self, *args, **kwargs):
        super().__init__(Requisites, *args, **kwargs)

    async def list(self, type_id: int):
        filters = [Requisites.type_id == type_id]
        return await self.fetch_all(None, filters)

    async def get_active(self, type_id: int) -> Requisites:
        sql = self.sql()
        sql = sql.where(
            Requisites.type_id == type_id,
            Requisites.is_active == True
        )
        return await self._fetch_first(sql)

    async def update(self, payload: schemas.RequisitesItemInput, session=None) -> None:
        if payload.is_active:
            sql = select(Requisites).options(load_only(Requisites.id)).where(
                Requisites.is_active == True,
                Requisites.type_id == payload.type_id
            )
            active_item = (await session.execute(sql)).scalars().first()
            if active_item:
                await session.execute(
                    update(Requisites).where(
                        Requisites.id == active_item.id
                    ).values(
                        is_active=False
                    )
                )
        values = strawberry_to_dict(payload, exclude_none=True, exclude={'id', 'type_id'})
        return await self.update_item(payload.id, values)

    async def create(self, payload: schemas.RequisitesCreateInput) -> dict:
        items: list[Requisites] = await self.list(payload.type_id)
        if len(items) > 0:
            is_active = False
        else:
            is_active = True
        payload_dict = strawberry_to_dict(payload)
        payload_dict['is_active'] = is_active
        return await self.create_item(payload_dict)

    async def delete(self, requisite_id: int) -> None:
        await self.delete_item(requisite_id)
