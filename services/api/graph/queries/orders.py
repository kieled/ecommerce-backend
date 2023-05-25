import strawberry

from config.db import session
from schemas import transaction_status_enum, OrderListType, OrderItemType
from services import OrderService
from utils import IsAdmin, orm_to_strawberry


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
        async with session() as s:
            data = await OrderService(s, info, page).list()
        return OrderListType(
            count=data.count,
            items=orm_to_strawberry(data.items, OrderItemType)
        )

    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Order detail info'
    )
    async def order_detail(self, order_id: int, info) -> OrderItemType:
        async with session() as s:
            data = await OrderService(s, info).detail(order_id)
        return orm_to_strawberry(data, OrderItemType)
