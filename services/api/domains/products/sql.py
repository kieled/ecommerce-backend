from sqlalchemy import select, Select
from sqlalchemy.orm import load_only, joinedload

from api.schemas import CreateOrderProductInput
from shared.db import Product, ProductParam, ProductImage, ProductCategory, ProductStock, ProductSize


def detail(product_id: int) -> Select:
    return select(Product).options(
        load_only(
            Product.title,
            Product.description,
            Product.price_buy,
            Product.price,
            Product.status,
            Product.ali_url,
            Product.inst_url
        ),
        joinedload(Product.params).load_only(
            ProductParam.name,
            ProductParam.value
        ),
        joinedload(Product.images).load_only(
            ProductImage.path
        ),
        joinedload(Product.category).load_only(
            ProductCategory.name,
            ProductCategory.slug
        ),
        joinedload(Product.stocks).load_only(
            ProductStock.name,
            ProductStock.color,
            ProductStock.image
        ).joinedload(ProductStock.sizes).load_only(
            ProductSize.size,
            ProductSize.name
        )
    ).where(Product.id == product_id)


def cart(products: list[CreateOrderProductInput]):
    return select(Product).options(
        load_only(Product.title, Product.price),
        joinedload(Product.stocks).load_only(
            ProductStock.name, ProductStock.color, ProductStock.image
        ).joinedload(ProductStock.sizes).load_only(
            ProductSize.size, ProductSize.name, ProductSize.product_stock_id
        )
    ).where(
        Product.id.in_([i.product_id for i in products])
    )
