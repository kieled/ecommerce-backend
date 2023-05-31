from datetime import datetime
import strawberry
from starlette.responses import Response
from strawberry.types import Info
from ..types import UpdateOrderInput, CreateOrderInput, CreatedOrderIdType
from ..bl import OrderBL
from api.domains.users.features.auth import IsAdmin


@strawberry.type
class OrderMutations:
    @strawberry.mutation(
        permission_classes=[IsAdmin],
        description='Update order info'
    )
    async def update_order(
            self,
            order: UpdateOrderInput,
            info: Info
    ) -> None:
        """ Update order mutation """
        return await OrderBL(info).update(order)

    @strawberry.mutation(
        description='Create new order'
    )
    async def create_order(
            self,
            payload: CreateOrderInput,
            info: Info
    ) -> CreatedOrderIdType:
        """ Create order from cart """
        data = await OrderBL(info).create(payload)
        if data['temp_id'] and not data['user_id']:
            now = datetime.now()
            expires = int((datetime(
                day=now.day,
                month=now.month,
                year=now.year + 1
            )).timestamp())
            response: Response = info.context['response']
            response.set_cookie('tempId', data['temp_id'], expires=expires)
        return CreatedOrderIdType(id=data['id'])
