from alchemy_graph import strawberry_to_dict
from sqlalchemy.ext.asyncio import AsyncSession

from shared.localizations import telegram as localizations
from shared.db import Order, Transaction, TransactionStatusEnum, cls_session
from shared.schemas import MessageSchema

from api.domains.users.features.auth import get_user_ids
from api.domains.mixin import AbstractBL
from api.domains.products.features.cart import CartInput
from api.broker import rabbit_connection

from . import sql
from .types import UpdateOrderInput


@cls_session
class OrderBL(AbstractBL[Order]):

    @staticmethod
    async def send_message(order_id: int, message: str, session=None) -> None:
        query = sql.order_telegram_ids(order_id)
        order = (await session.execute(query)).scalars().first()

        if order and order.customer_address.user.telegram_chat_id:
            await rabbit_connection.send_messages(MessageSchema(
                action='telegram:order_message',
                body={
                    'telegram_chat_id': order.customer_address.user.telegram_chat_id,
                    'order_id': order.id,
                    'message': message
                }
            ))

    async def list(self, session: AsyncSession = None):
        filters = (Order.transaction.has(Transaction.status == TransactionStatusEnum.complete),)
        return await self.list_items(session, 'items', filters)

    async def detail(self, order_id: int, session: AsyncSession = None):
        order = await self.fetch_one(order_id, session)
        if not order:
            raise Exception('Not found')
        return order

    async def update(self, payload: UpdateOrderInput, session: AsyncSession = None):
        update_dict = strawberry_to_dict(payload, exclude={'order_id'}, exclude_none=True)
        message = {
            'order_url': localizations.order_confirmed_message,
            'track_code': localizations.track_code_message(payload.track_code or '')
        }
        if payload.order_url or payload.track_code:
            await self.send_message(
                payload.order_id,
                message['order_url'] if payload.order_id else message['track_code']
            )
        await self.update_item(
            payload.order_id,
            update_dict,
            session=session
        )

    async def create(self, payload: CartInput, transaction_id: int, session: AsyncSession = None):
        temp_user_id, user_id = get_user_ids(self.info)

        await self.create_item([
            dict(
                count=i.count,
                customer_address_id=payload.address_id,
                transaction_id=transaction_id,
                product_id=i.product_id,
                product_size_id=i.size_id,
                product_stock_id=i.color_id
            ) for i in payload.products
        ], session)

        return dict(id=transaction_id, temp_id=temp_user_id, user_id=user_id)
