from sqlalchemy import select
from sqlalchemy.orm import load_only, joinedload

from shared.db import Product, ProductStock, ProductSize


def cart(products):
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
