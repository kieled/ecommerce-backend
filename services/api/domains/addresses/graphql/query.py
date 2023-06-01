import strawberry
from alchemy_graph import orm_to_strawberry
from config import session
from parsers import prices_manager
from ..types import CustomerAddressType, CreateOrderProductInput, CustomerCardListType, CustomerCardType
from utils import IsAuthenticated
from ..bl import AddressBL


@strawberry.type
class AddressQuery:
    @strawberry.field(
        permission_classes=[IsAuthenticated],
        description='Customer addresses saved list'
    )
    async def customer_addresses(self, info) -> list[CustomerAddressType]:
        data = await AddressBL(info).address_list()
        return orm_to_strawberry(data, CustomerAddressType)
