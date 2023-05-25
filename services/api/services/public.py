from models import Product
from .mixins import AppService, ListType


class PublicService(AppService):
    def __init__(self, db, info, page: int | None = 1):
        super().__init__(db, Product, info, page=page, page_size=18)

    async def list(self, category_id: int):
        filters = []
        if category_id:
            filters.append(Product.category_id == category_id)
        else:
            items = await self._fetch_all(
                self._order(self.sql('products').limit(5))
            )
            return ListType(
                items=items,
                count=5
            )
        return await self.list_items('products', filters)

    async def detail(self, product_id: int) -> Product:
        data = await self.fetch_one(product_id)
        if not data:
            raise Exception('Not found')
        return data
