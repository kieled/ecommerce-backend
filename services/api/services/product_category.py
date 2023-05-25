import utils
from models import ProductCategory
from schemas import UpdateProductCategoryInput, ProductCategoryInput
from .mixins import AppService


class ProductCategoryService(AppService):
    def __init__(self, db, info, *args):
        super().__init__(db, ProductCategory, info, *args)

    async def list(self) -> list[ProductCategory]:
        return await self._fetch_all(
            self._paginate(self.sql())
        )

    async def create(self, payload: ProductCategoryInput) -> dict:
        payload_dict = strawberry_to_dict(payload)
        return await self.create_item(payload_dict)

    async def update(self, payload: UpdateProductCategoryInput) -> dict:
        payload_dict = strawberry_to_dict(payload, exclude={'id'})
        await self.update_item(payload.id, payload_dict)
        return strawberry_to_dict(payload)

    async def delete(self, category_id: int) -> None:
        await self.delete_item(category_id)
