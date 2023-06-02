from sqlalchemy import select, Select
from sqlalchemy.orm import load_only, joinedload

from api.domains.products.features.cart import CartProductInput
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


def only_prices(products: list[CartProductInput]):
    return select(Product).options(
        load_only(Product.price)
    ).where(
        Product.id.in_([p.product_id for p in products])
    )
