from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ..config import Base


class Order(Base):
    from .product import ProductSize, ProductStock, Product
    from .user import CustomerAddress
    from .transaction import Transaction

    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)

    count: Mapped[int]
    track_code: Mapped[str | None]
    order_url: Mapped[str | None]

    customer_address_id: Mapped[int] = mapped_column(ForeignKey('customer_addresses.id'))
    transaction_id: Mapped[int] = mapped_column(ForeignKey('transactions.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product_size_id: Mapped[int | None] = mapped_column(ForeignKey('product_size.id'))
    product_stock_id: Mapped[int | None] = mapped_column(ForeignKey('product_stock.id'))

    product_size: Mapped[ProductSize] = relationship(
        lazy=True
    )
    product_stock: Mapped[ProductStock] = relationship(
        lazy=True
    )
    product: Mapped[Product] = relationship(
        lazy=True
    )
    customer_address: Mapped[CustomerAddress] = relationship(
        back_populates='orders',
        lazy=True
    )
    transaction: Mapped[Transaction] = relationship(
        back_populates='orders',
        lazy=True
    )
