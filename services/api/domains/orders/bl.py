import math
import string
import random

from alchemy_graph import strawberry_to_dict
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, joinedload
from shared.localizations import telegram as localizations
from shared.db import Order, CustomerAddress, Transaction, Requisites, Product, TransactionCurrencyEnum, Promo, \
    RequisiteTypes, TransactionStatusEnum, cls_session
from api.domains.users.features.auth import get_user_ids
from api.domains.mixin import AbstractBL
from shared.schemas import MessageSchema
from . import sql
from api.broker import rabbit_connection
from .types import UpdateOrderInput, CreateOrderInput


@cls_session
class OrderBL(AbstractBL[Order]):
    def __init__(self, info, *args, **kwargs):
        super().__init__(Order, info, *args, **kwargs)

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

    async def create(self, payload: CreateOrderInput, session: AsyncSession = None):
        temp_user_id, user_id = get_user_ids(self.info)

        if not temp_user_id and not user_id:
            temp_user_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))

        if payload.address and payload.address_id is not None:
            raise Exception('You should use only address or address_id fields')

        if payload.address:
            address_id = await CustomerService(session, self.info).create_address(payload.address, temp_user_id)
        else:
            address_id = payload.address_id

        address = (await session.execute(
            select(CustomerAddress.id).where(CustomerAddress.id == address_id)
        )).scalars().first()

        if not address:
            raise Exception('Required address_id or address fields or incorrect address_id')

        promo = None
        if payload.promo:
            sql = select(Promo).where(
                Promo.code == payload.promo,
                ~Promo.transaction.has()
            )
            promo = (await session.execute(sql)).scalars().first()

        product_prices = (await session.execute(
            select(Product).options(
                load_only(Product.price)
            ).where(
                Product.id.in_([p.product_id for p in payload.products])
            )
        )).scalars().all()

        amount = 0

        for i in product_prices:
            count = next((p.count for p in payload.products if p.product_id == i.id), None)
            if count is None:
                continue
            amount += i.price * count

        if amount == 0:
            return

        sql = select(Requisites).options(
            load_only(Requisites.id),
            joinedload(Requisites.type).load_only(RequisiteTypes.currency)
        ).where(
            Requisites.type_id == payload.payment_type,
            Requisites.is_active == True
        )

        requisite = (await session.execute(sql)).scalars().first()

        if not requisite:
            raise Exception('Not any transactions available now')

        currency_type = TransactionCurrencyEnum(requisite.type.currency).value if requisite.type.currency else None

        if promo:
            amount = math.ceil(amount - amount * promo.discount)

        transaction_id = (await session.execute(
            insert(Transaction).values(
                amount=amount,
                promo_id=promo.id if promo else None,
                currency=currency_type if currency_type else '$',
                user_id=user_id,
                temp_user_id=temp_user_id,
                requisite_id=requisite.id
            ).returning(Transaction.id)
        )).scalars().first()

        if not transaction_id:
            raise Exception("Order couldn't be created")

        await session.execute(
            insert(Order).values([
                dict(
                    count=i.count,
                    customer_address_id=address_id,
                    transaction_id=transaction_id,
                    product_id=i.product_id,
                    product_size_id=i.size_id,
                    product_stock_id=i.color_id
                ) for i in payload.products
            ])
        )

        await session.commit()
        return dict(id=transaction_id, temp_id=temp_user_id, user_id=user_id)
