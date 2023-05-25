import asyncio
import aiohttp
from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only
import utils
from models import Product, ProductImage, ProductStock, ProductSize, ProductParam, ProductCategory
from schemas import ProductCreateInput, ProductUpdateInput
from .mixins import AppService


class ProductService(AppService):
    def __init__(self, db, *args):
        super().__init__(db, Product, *args)

    async def list(
            self,
            search_id: int | None = None,
            category_id: int | None = None
    ):
        filters = []
        if search_id:
            filters.append(Product.id == search_id)
        if category_id:
            filters.append(Product.category_id == category_id)

        return await self.list_items('products', filters)

    async def detail(self, product_id: int):
        product = await self.fetch_one(product_id)
        if not product:
            raise Exception('Not found')
        return product

    async def detail_full(self, product_id: int) -> Product:
        sql = select(Product).options(
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
        return (await self.db.execute(sql)).scalars().first()

    async def create(self, payload: ProductCreateInput) -> int:
        product = Product(
            params=[
                ProductParam(name=param.name, value=param.value) for param in payload.params
            ],
            **strawberry_to_dict(
                payload, exclude={'images', 'stocks', 'params', 'url'}
            ),
            ali_url=payload.url
        )
        self.db.add(product)
        await self.db.flush()
        async with aiohttp.ClientSession() as s:
            product_images = await asyncio.gather(*[utils.handle_image(
                product.id,
                value,
                session=s,
                folder='default',
                filename=str(index + 1)
            ) for index, value in enumerate(payload.images)])
            self.db.add_all([ProductImage(path=p, product_id=product.id) for p in product_images])
            stock_images = await asyncio.gather(*[
                utils.handle_image(
                    product.id,
                    stock.image,
                    session=s,
                    folder='colors',
                    filename=str(index + 1)
                ) for index, stock in enumerate(payload.stocks)
            ])
            self.db.add_all(
                [ProductStock(
                    name=stock.name if stock.name else None,
                    color=stock.color,
                    image=stock_images[index],
                    product_id=product.id,
                    sizes=[
                        ProductSize(size=size.size, name=size.name) for size in stock.sizes
                    ]
                ) for index, stock in enumerate(payload.stocks)]
            )
        await self.db.commit()
        return product.id

    async def update(self, payload: ProductUpdateInput) -> None:
        product_updates = strawberry_to_dict(payload, exclude_none=True, exclude={'product_id'})
        await self.update_item(payload.product_id, product_updates)

    async def delete(self, product_id: int) -> None:
        await self.delete_item(product_id)
