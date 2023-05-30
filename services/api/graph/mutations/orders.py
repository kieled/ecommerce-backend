from datetime import datetime
import strawberry
from starlette.responses import Response
from strawberry.types import Info

from api.config import rabbit_connection
from api.schemas import UpdateOrderInput, CreateOrderInput, CreatedOrderIdType
from api.services import OrderService, TransactionService
from api.utils import IsAdmin
from shared.schemas import MessageSchema


@strawberry.type
class OrderMutation:
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
        return await OrderService(info).update(order)

    @strawberry.mutation(
        description='Create new order'
    )
    async def create_order(
            self,
            payload: CreateOrderInput,
            info: Info
    ) -> CreatedOrderIdType:
        """ Create order from cart """
        data = await OrderService(info).create(payload)
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

    @strawberry.mutation(
        description='Create new order'
    )
    async def confirm_public_order(
            self,
            order_id: int,
            info: Info
    ) -> None:
        """ Confirm payment public order """
        data = await TransactionService(info).confirm_public_payment(order_id)
        await rabbit_connection.send_messages(MessageSchema(
            action='payment:check',
            body=data
        ))
