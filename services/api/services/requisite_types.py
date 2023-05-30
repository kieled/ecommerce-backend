from alchemy_graph import strawberry_to_dict

from shared.db import RequisiteTypes
from api.schemas import RequisiteTypeItemInput, RequisiteTypeCreateInput
from .mixins import AppService


class RequisiteTypesService(AppService):
    def __init__(self, *args, **kwargs):
        super().__init__(RequisiteTypes, *args, **kwargs)

    async def list(self):
        return await self.fetch_all()

    async def create(self, payload: RequisiteTypeCreateInput):
        payload_dict = strawberry_to_dict(payload)
        return await self.create_item(payload_dict)

    async def delete(self, type_id: int):
        await self.delete_item(type_id)

    async def update(self, payload: RequisiteTypeItemInput):
        payload_dict = strawberry_to_dict(payload, exclude_none=True, exclude={'id'})
        await self.update_item(
            payload.id,
            payload_dict
        )
