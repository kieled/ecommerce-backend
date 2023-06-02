import aiohttp
from alchemy_graph import strawberry_to_dict
from sqlalchemy.ext.asyncio import AsyncSession
from shared.db import Product, ProductParam, cls_session
from .features.cart import CartProductInput
from .features.images import prepare_images
from .types import ProductCreateInput, ProductUpdateInput
from api.domains.mixin import AbstractBL
from . import sql


@cls_session
class ProductBL(AbstractBL[Product]):

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
            product_images, stock_images = await prepare_images(product.id, s, payload)
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

    async def calc_prices(self, items: list[CartProductInput], session: AsyncSession = None) -> int:
        product_prices = await self._fetch_all(sql.only_prices(items), session)

        amount = 0

        for i in product_prices:
            count = next((p.count for p in items if p.product_id == i.id), None)
            if count is None:
                continue
            amount += i.price * count

        if amount == 0:
            raise Exception('Bad request')

        return amount
