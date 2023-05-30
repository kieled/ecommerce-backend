from alchemy_graph import strawberry_to_dict
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info

from api.schemas import CustomerAddressInput
from api.utils import AppService, get_user_ids
from shared.db import CustomerAddress, cls_session


@cls_session
class AddressBL(AppService[CustomerAddress]):
    def __init__(self, info: Info):
        super().__init__(CustomerAddress, info)

    async def address_list(self, session: AsyncSession = None):
        temp_user_id, user_id = get_user_ids(self.info)

        filters = (CustomerAddress.user_id == user_id,)
        if temp_user_id:
            filters = (CustomerAddress.temp_user_id == temp_user_id,)
        return await self.fetch_all(filters=filters, session=session)

    async def create_address(
            self,
            payload: CustomerAddressInput,
            temp_user_id: str | None = None,
            session: AsyncSession = None
    ):
        user_id: int = self.info.context.get('user_id')
        return await self.create_item(
            payload=dict(
                **strawberry_to_dict(payload, exclude_none=True),
                user_id=user_id,
                temp_user_id=temp_user_id
            ),
            session=session
        )
