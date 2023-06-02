from __future__ import annotations

from datetime import datetime

from ..config import Base
from ..enums import TransactionStatusEnum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Transaction(Base):
    from .order import Order
    from .user import User

    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[TransactionStatusEnum] = mapped_column(default=TransactionStatusEnum.created)
    promo_id: Mapped[int | None] = mapped_column(ForeignKey('promo_codes.id'))
    amount: Mapped[int]
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    temp_user_id: Mapped[str | None]
    requisite_id: Mapped[int] = mapped_column(ForeignKey('requisites.id'))
    bank_number_id: Mapped[str | None]

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )

    promo: Mapped[Promo] = relationship(
        lazy=True,
        back_populates='transaction'
    )

    orders: Mapped[list[Order]] = relationship(
        lazy=True,
        back_populates='transaction'
    )

    user: Mapped[User] = relationship(
        lazy=True,
        back_populates='transactions'
    )

    requisite: Mapped[Requisites] = relationship(
        lazy=True
    )

    __mapper_args__ = {"eager_defaults": True}


class RequisiteTypes(Base):
    __tablename__ = 'requisite_types'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    detail: Mapped[str]


class Requisites(Base):
    __tablename__ = 'requisites'

    id: Mapped[int] = mapped_column(primary_key=True)

    type_id: Mapped[int] = mapped_column(ForeignKey('requisite_types.id'))
    info: Mapped[str]
    detail: Mapped[str | None]
    is_active: Mapped[bool]

    type: Mapped[RequisiteTypes] = relationship(
        lazy=True
    )


class Promo(Base):
    __tablename__ = 'promo_codes'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str]
    discount: Mapped[float]

    transaction: Mapped[Transaction] = relationship(
        lazy=True,
        back_populates='promo',
        uselist=False
    )
