from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from ..config import Base
from ..enums import UserTypeEnum


class User(Base):
    from .transaction import Transaction

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[UserTypeEnum] = mapped_column(default=UserTypeEnum.user)
    username: Mapped[str | None]
    password: Mapped[str | None]

    telegram_chat_id: Mapped[str | None]
    image_url: Mapped[str | None]
    first_name: Mapped[str | None]

    addresses: Mapped[list[CustomerAddress]] = relationship(
        lazy=True,
        back_populates='user'
    )

    transactions: Mapped[list[Transaction]] = relationship(
        lazy=True,
        back_populates='user'
    )


class CustomerAddress(Base):
    from .order import Order

    __tablename__ = 'customer_addresses'

    id: Mapped[int] = mapped_column(primary_key=True)

    flat: Mapped[int | None]
    house: Mapped[str]
    street: Mapped[str]
    city: Mapped[str]
    region: Mapped[str]
    postal_index: Mapped[int]
    first_name: Mapped[str]
    last_name: Mapped[str]
    country: Mapped[str]

    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    temp_user_id: Mapped[str | None]

    user: Mapped[User] = relationship(
        lazy=True,
        back_populates='addresses'
    )

    orders: Mapped[list[Order]] = relationship(
        lazy=True,
        back_populates='customer_address'
    )
