from alchemy_graph import strawberry_to_dict
from sqlalchemy.ext.asyncio import AsyncSession
from api.domains.mixin import AbstractBL
from api.utils.graphql import get_user_ids
from shared.db import CustomerAddress, cls_session
from . import sql
from .types import AddressInput


@cls_session
class AddressBL(AbstractBL[CustomerAddress]):

    async def address_list(self, session: AsyncSession = None):
        temp_user_id, user_id = get_user_ids(self.info)

        filters = (CustomerAddress.user_id == user_id,)
        if temp_user_id:
            filters = (CustomerAddress.temp_user_id == temp_user_id,)
        return await self.fetch_all(filters=filters, session=session)

    async def get_or_create(
            self,
            payload: AddressInput,
            temp_user_id: str | None,
            session: AsyncSession = None
    ) -> int | None:
        if payload.address and payload.address_id is not None:
            raise Exception('You should use only address or address_id fields')

        if payload.address:
            user_id: int = self.info.context.get('user_id')
            data = await self.create_item(
                payload=dict(
                    **strawberry_to_dict(payload, exclude_none=True),
                    user_id=user_id,
                    temp_user_id=temp_user_id
                ),
                session=session
            )
            address_id = data.id
        else:
            address_id = payload.address_id

        address: int | None = await self._fetch_first(sql.exists_by_id(address_id), session)

        if address is None:
            raise Exception('Required address_id or address fields or incorrect address_id')

        return address
