from __future__ import annotations

from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from ..config import Base

from ..enums import ProductStatusEnum, TransactionStatusEnum, UserTypeEnum

__all__ = [
    'Requisites',
    'CustomerAddress',
    'User',
    'Promo',
    'ProductStock',
    'ProductSize',
    'ProductParam',
    'ProductCategory',
    'Order',
    'RequisiteTypes',
    'ProductImage',
    'Product',
    'Transaction',
    'Base'
]


class Order(Base):
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


class ProductImage(Base):
    __tablename__ = 'product_images'

    id: Mapped[int] = mapped_column(primary_key=True)

    path: Mapped[str]
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))

    product: Mapped[Product] = relationship(
        back_populates='images',
        lazy=True
    )


class ProductSize(Base):
    __tablename__ = 'product_size'

    id: Mapped[int] = mapped_column(primary_key=True)
    size: Mapped[str]
    name: Mapped[str | None]
    product_stock_id: Mapped[int] = mapped_column(ForeignKey('product_stock.id'))

    product_stock: Mapped[ProductStock] = relationship(
        lazy=True,
        back_populates='sizes'
    )


class ProductStock(Base):
    __tablename__ = 'product_stock'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None]
    color: Mapped[str]
    image: Mapped[str]
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))

    product: Mapped[Product] = relationship(lazy=True, back_populates='stocks')
    sizes: Mapped[list[ProductSize]] = relationship(
        lazy=True,
        back_populates='product_stock',
        cascade="all, delete-orphan",
        order_by='ProductSize.id'
    )


class ProductParam(Base):
    __tablename__ = 'product_params'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    value: Mapped[str]

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))

    product: Mapped[Product] = relationship(
        lazy=True,
        back_populates='params'
    )


class ProductCategory(Base):
    __tablename__ = 'product_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    slug: Mapped[str]


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]
    status: Mapped[ProductStatusEnum] = mapped_column(default=ProductStatusEnum.created)
    price_buy: Mapped[int] = mapped_column(default=0)
    price: Mapped[int] = mapped_column(default=0)
    inst_url: Mapped[str | None]
    ali_url: Mapped[str | None]
    description: Mapped[str]
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    category_id: Mapped[int | None] = mapped_column(ForeignKey('product_categories.id', ondelete='CASCADE'))

    images: Mapped[list[ProductImage]] = relationship(
        back_populates='product',
        order_by='ProductImage.id',
        lazy=True
    )
    category: Mapped[ProductCategory] = relationship(
        lazy=True
    )
    stocks: Mapped[list[ProductStock]] = relationship(
        back_populates='product',
        lazy=True,
        cascade="all, delete-orphan"
    )
    params: Mapped[list[ProductParam]] = relationship(
        lazy=True,
        back_populates='product',
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {"eager_defaults": True}


class Transaction(Base):
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


class User(Base):
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
