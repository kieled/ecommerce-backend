import strawberry
from config import session
from parsers import prices_manager
from schemas import CustomerAddressType, CreateOrderProductInput, CustomerCardListType, CustomerCardType
from services import CustomerService
from utils import IsAuthenticated, orm_to_strawberry


@strawberry.type
class CustomerQuery:
    @strawberry.field(
        permission_classes=[IsAuthenticated],
        description='Customer addresses saved list'
    )
    async def customer_addresses(self, info) -> list[CustomerAddressType]:
        async with session() as s:
            data = await CustomerService(s, info).address_list()
        return orm_to_strawberry(data, CustomerAddressType)

    @strawberry.field(
        description='Detail info about customer cart'
    )
    async def customer_cart(
            self,
            products: list[CreateOrderProductInput],
            info
    ) -> CustomerCardListType:
        prices = await prices_manager.get()
        async with session() as s:
            data = await CustomerService(s, info).get_cart_products(prices, products)
        return CustomerCardListType(
            items=[CustomerCardType(**i) for i in data['items']],
            sum=data['sum']
        )
