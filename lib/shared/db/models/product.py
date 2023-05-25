from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from ..config import Base
from ..enums import ProductStatusEnum


class ProductImage(Base):
    __tablename__ = 'product_images'

    id: Mapped[int] = mapped_column(primary_key=True)

    path: Mapped[str]
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))

    product: Mapped['Product'] = relationship(
        back_populates='images',
        lazy=True
    )


class ProductSize(Base):
    __tablename__ = 'product_size'

    id: Mapped[int] = mapped_column(primary_key=True)
    size: Mapped[str]
    name: Mapped[str | None]
    product_stock_id: Mapped[int] = mapped_column(ForeignKey('product_stock.id'))

    product_stock: Mapped['ProductStock'] = relationship(
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

    product: Mapped['Product'] = relationship(lazy=True, back_populates='stocks')
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

    product: Mapped['Product'] = relationship(
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
