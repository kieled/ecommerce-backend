from sqlalchemy import insert, select, desc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, joinedload
from strawberry.types import Info
import utils
from models import CustomerAddress, Product, ProductSize, ProductStock
import schemas
from utils import convert_price, get_user_ids
from .mixins import get_selected_sql


class CustomerService:
    def __init__(self, db: AsyncSession, info: Info):
        self.db = db
        self.info = info

    async def address_list(self):
        temp_user_id, user_id = get_user_ids(self.info)
        if temp_user_id:
            filters = (CustomerAddress.temp_user_id == temp_user_id,)
        else:
            filters = (CustomerAddress.user_id == user_id,)
        sql = get_selected_sql(CustomerAddress, self.info)()
        sql = sql.where(*filters)
        sql = sql.order_by(desc(CustomerAddress.id))

        return (await self.db.execute(sql)).scalars().unique().all()

    async def create_address(self, payload: schemas.CustomerAddressInput, temp_user_id: str | None = None) -> int:
        payload_dict = strawberry_to_dict(payload, exclude_none=True)
        user_id = self.info.context.get('user_id')
        if user_id:
            user_id = int(user_id)
        sql = insert(CustomerAddress).values(
            **payload_dict,
            user_id=user_id,
            temp_user_id=temp_user_id
        ).returning(CustomerAddress.id)

        address_id = (await self.db.execute(sql)).scalars().first()
        await self.db.commit()
        return address_id

    async def get_cart_products(self, prices: dict, products: list[schemas.CreateOrderProductInput]):
        sql = select(Product).options(
            load_only(Product.title, Product.price),
            joinedload(Product.stocks).load_only(
                ProductStock.name, ProductStock.color, ProductStock.image
            ).joinedload(ProductStock.sizes).load_only(
                ProductSize.size, ProductSize.name, ProductSize.product_stock_id
            )
        ).where(
            Product.id.in_([i.product_id for i in products])
        )
        result = (await self.db.execute(sql)).scalars().unique().all()
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
                dict(
                    product_id=product.id,
                    size_id=product_input.size_id,
                    price=convert_price(amount, prices, self.info),
                    size=size,
                    image=stock.image,
                    stock=stock.name if stock.name else stock.color,
                    title=product.title,
                    count=product_input.count,
                )
            )
        total_price = convert_price(total_price, prices, self.info)
        return dict(
            items=result_products,
            sum=total_price
        )
