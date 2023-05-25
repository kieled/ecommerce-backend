import math
import string
import random

from alchemy_graph import strawberry_to_dict
from sqlalchemy import select, insert
from sqlalchemy.orm import load_only, joinedload
from shared.localizations import telegram as localizations
from shared.db import User, Order, CustomerAddress, Transaction, Requisites, Product, TransactionCurrencyEnum, Promo, \
    RequisiteTypes, TransactionStatusEnum
from api import schemas
from api.utils import get_user_ids
from shared.schemas import MessageSchema
from .customers import CustomerService
from .mixins import AppService
from ..config import rabbit_connection


class OrderService(AppService):
    def __init__(self, db, info, *args):
        super().__init__(db, Order, info, *args)

    async def send_message(self, order_id: int, message: str):
        sql = select(Order).options(
            load_only(Order.id),
            joinedload(Order.customer_address).load_only(
                CustomerAddress.id
            ).joinedload(CustomerAddress.user).load_only(
                User.telegram_chat_id
            )
        ).where(
            Order.id == order_id
        )

        order = (await self.db.execute(sql)).scalars().first()

        if order and order.customer_address.user.telegram_chat_id:
            await rabbit_connection.send_messages(MessageSchema(action='telegram:order_message', body={
                'telegram_chat_id': order.customer_address.user.telegram_chat_id,
                'order_id': order.id,
                'message': message
            }))

    async def list(self):
        filters = [
            Order.transaction.has(Transaction.status == TransactionStatusEnum.complete)
        ]
        return await self.list_items('items', filters)

    async def detail(self, order_id: int):
        order = await self.fetch_one(order_id)
        if not order:
            raise Exception('Not found')
        return order

    async def update(self, payload: schemas.UpdateOrderInput):
        update_dict = strawberry_to_dict(payload, exclude={'order_id'}, exclude_none=True)
        if payload.order_url:
            await self.send_message(
                payload.order_id,
                localizations.order_confirmed_message
            )
        if payload.track_code:
            await self.send_message(
                payload.order_id,
                localizations.track_code_message(payload.track_code)
            )
        await self.update_item(
            payload.order_id,
            update_dict
        )

    async def create(self, payload: schemas.CreateOrderInput):
        temp_user_id, user_id = get_user_ids(self.info)

        if not temp_user_id and not user_id:
            temp_user_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))

        if payload.address and payload.address_id is not None:
            raise Exception('You should use only address or address_id fields')

        if payload.address:
            address_id = await CustomerService(self.db, self.info).create_address(payload.address, temp_user_id)
        else:
            address_id = payload.address_id

        address = (await self.db.execute(
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
            promo = (await self.db.execute(sql)).scalars().first()

        product_prices = (await self.db.execute(
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

        requisite = (await self.db.execute(sql)).scalars().first()

        if not requisite:
            raise Exception('Not any requisites available now')

        currency_type = TransactionCurrencyEnum(requisite.type.currency).value if requisite.type.currency else None

        if promo:
            amount = math.ceil(amount - amount * promo.discount)

        transaction_id = (await self.db.execute(
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

        await self.db.execute(
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

        await self.db.commit()
        return dict(id=transaction_id, temp_id=temp_user_id, user_id=user_id)
