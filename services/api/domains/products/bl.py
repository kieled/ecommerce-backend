import asyncio
import aiohttp
from alchemy_graph import strawberry_to_dict
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info

from shared.db import Product, ProductImage, ProductStock, ProductSize, ProductParam, cls_session
from api.schemas import ProductCreateInput, ProductUpdateInput, CreateOrderProductInput
from api.utils import AppService, handle_image
from . import sql


@cls_session
class ProductBL(AppService[Product]):
    def __init__(self, info: Info, *args, **kwargs):
        super().__init__(Product, info, *args, **kwargs)

    async def items(
            self,
            search_id: int | None = None,
            category_id: int | None = None,
            session: AsyncSession = None
    ):
        filters = []
        if search_id:
            filters.append(Product.id == search_id)
        if category_id:
            filters.append(Product.category_id == category_id)

        return await self.list_items(session, 'products', filters)

    async def detail(self, product_id: int, session: AsyncSession = None) -> Product:
        return await self.fetch_one(product_id, session)

    @staticmethod
    async def detail_full(product_id: int, session=None) -> Product:
        return (await session.execute(
            sql.detail(product_id)
        )).scalars().first()

    @staticmethod
    async def _download_images(product_id: int, s: aiohttp.ClientSession, payload: ProductCreateInput):
        product_images = await asyncio.gather(*[handle_image(
            product_id,
            value,
            session=s,
            folder='default',
            filename=str(index + 1)
        ) for index, value in enumerate(payload.images)])
        stock_images = await asyncio.gather(*[
            handle_image(
                product_id,
                stock.image,
                session=s,
                folder='colors',
                filename=str(index + 1)
            ) for index, stock in enumerate(payload.stocks)
        ])
        return (
            [ProductImage(path=p, product_id=product_id) for p in product_images],
            [ProductStock(name=stock.name if stock.name else None, color=stock.color,
                          image=stock_images[index], product_id=product_id,
                          sizes=[ProductSize(size=size.size, name=size.name) for size in stock.sizes]
                          ) for index, stock in enumerate(payload.stocks)
             ]
        )

    async def create(self, payload: ProductCreateInput, session: AsyncSession = None) -> Product:
        product = Product(
            params=[
                ProductParam(name=param.name, value=param.value) for param in payload.params
            ],
            **strawberry_to_dict(
                payload, exclude={'images', 'stocks', 'params', 'url'}
            ),
            ali_url=payload.url
        )
        session.add(product)
        await session.flush()
        async with aiohttp.ClientSession() as s:
            product_images, stock_images = await self._download_images(product.id, s, payload)
            session.add_all([*product_images, *stock_images])
        await session.commit()
        return product

    async def update(self, payload: ProductUpdateInput, session: AsyncSession = None) -> None:
        product_updates = strawberry_to_dict(payload, exclude_none=True, exclude={'product_id'})
        await self.update_item(payload.product_id, product_updates, session)

    async def delete(self, product_id: int, session: AsyncSession = None) -> None:
        await self.delete_item(product_id, session)

    async def public_list(self, category_id: int, session: AsyncSession = None):
        filters = tuple()
        if category_id:
            filters = (Product.category_id == category_id,)
        return await self.list_items(
            session,
            inner='products',
            filters=filters,
            limit=18 if category_id else 5
        )

    async def public_detail(self, product_id: int, session: AsyncSession = None):
        return await self.fetch_one(product_id, session)

    @staticmethod
    async def cart_products(products: list[CreateOrderProductInput], session: AsyncSession = None):
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
                dict(
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
        return dict(
            items=result_products,
            sum=total_price
        )
