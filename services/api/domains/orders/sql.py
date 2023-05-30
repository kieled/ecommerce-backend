from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import select

from shared.db import Order, CustomerAddress, User


def order_telegram_ids(order_id: int):
    return select(Order).options(
        load_only(Order.id),
        joinedload(Order.customer_address).load_only(
            CustomerAddress.id
        ).joinedload(CustomerAddress.user).load_only(
            User.telegram_chat_id
        )
    ).where(
        Order.id == order_id
    )
