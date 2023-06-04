import strawberry
from alchemy_graph import orm_to_strawberry

from ..bl import OrderBL
from ..types import OrderListType, OrderItemType
from api.utils.graphql import IsAdmin


@strawberry.type
class OrderQuery:
    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Orders list'
    )
    async def orders(
            self,
            info,
            page: int | None = 1
    ) -> OrderListType:
        data = await OrderBL(info, page=page).list()
        return orm_to_strawberry(data, OrderListType)

    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Order detail info'
    )
    async def order_detail(self, order_id: int, info) -> OrderItemType:
        data = await OrderBL(info).detail(order_id)
        return orm_to_strawberry(data, OrderItemType)
