from sqlalchemy.ext.asyncio import AsyncSession

from shared.db import session_wrap
from . import sql
from .types import CartType, CartProductType


@session_wrap
async def cart_products(products, session: AsyncSession = None):
    result = (await session.execute(
        sql.cart(products)
    )).scalars().unique().all()
    total_price = 0
    result_products = []

    def get_product(product_id: int):
        return next((i for i in result if i.id == product_id), None)

    def get_stock(item, stock_id: int):
        return next((i for i in item.stocks if i.id == stock_id), None)

    def get_size(item, size_id: int):
        return next((d for i in item.stocks for d in i.sizes if d.id == size_id), None)

    for product_input in products:
        product = get_product(product_input.product_id)
        if not product:
            continue
        size = get_size(product, product_input.size_id) if product_input.size_id else None
        if size:
            stock = get_stock(product, size.product_stock_id)
            size = size.name or size.size
        else:
            stock = get_stock(product, product_input.color_id) if product_input.color_id else None

        amount = product.price * product_input.count
        total_price += amount
        result_products.append(
            CartProductType(
                product_id=product.id,
                size_id=product_input.size_id,
                price=amount,
                size=size,
                image=stock.image,
                stock=stock.name if stock.name else stock.color,
                title=product.title,
                count=product_input.count,
            )
        )
    return CartType(
        items=result_products,
        sum=total_price
    )
