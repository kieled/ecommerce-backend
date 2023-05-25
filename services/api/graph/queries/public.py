import strawberry
from strawberry.types import Info
from config import session
from parsers import prices_manager
from schemas import PublicListType, PublicDetailType
from services import PublicService
from utils import orm_to_strawberry, convert_price


@strawberry.type
class PublicQuery:
    @strawberry.field
    async def products_public(
            self,
            info: Info,
            page: int | None = 1,
            category_id: int | None = None
    ) -> PublicListType:
        """ Public products list """
        async with session() as s:
            prices = await prices_manager.get()
            data = await PublicService(s, info, page).list(category_id)
        products = data.items
        for i, product in enumerate(products):
            product.images = products[i].images[:1]
            product.price = convert_price(product.price, prices, info)
        return orm_to_strawberry(dict(
            count=data.count,
            products=products
        ), PublicListType)

    @strawberry.field
    async def public_detail(self, info, product_id: int) -> PublicDetailType:
        """ Public product detail """
        async with session() as s:
            data = await PublicService(s, info).detail(product_id)
        prices = await prices_manager.get()
        data.price = convert_price(data.price, prices, info)
        return orm_to_strawberry(data, PublicDetailType)
