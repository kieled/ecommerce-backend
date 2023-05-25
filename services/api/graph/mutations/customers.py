import strawberry
from alchemy_graph import strawberry_to_dict
from strawberry.types import Info
from api.schemas import CustomerAddressInput, CustomerAddressType
from api.services import CustomerService
from api.utils import IsAuthenticated
from shared.db import scoped_session


@strawberry.type
class CustomersMutation:
    @strawberry.mutation(
        permission_classes=[IsAuthenticated],
        description='Add new customer address'
    )
    async def add_address(
            self,
            payload: CustomerAddressInput,
            info: Info
    ) -> CustomerAddressType:
        async with scoped_session() as s:
            address_id = await CustomerService(s, info).create_address(payload)
        return CustomerAddressType(
            id=address_id,
            **strawberry_to_dict(payload)
        )
