from alchemy_graph import strawberry_to_dict
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db import ProductCategory, cls_session
from .types import UpdateProductCategoryInput, ProductCategoryInput
from api.domains.mixin import AbstractBL


@cls_session
class ProductCategoryBL(AbstractBL[ProductCategory]):
    
    async def list(self, session: AsyncSession = None):
        return await self.fetch_all(session)

    async def create(self, payload: ProductCategoryInput, session: AsyncSession = None) -> ProductCategory:
        payload_dict = strawberry_to_dict(payload)
        return await self.create_item(payload_dict, session)

    async def update(self, payload: UpdateProductCategoryInput, session: AsyncSession = None):
        payload_dict = strawberry_to_dict(payload, exclude={'id'})
        await self.update_item(payload.id, payload_dict, session)

    async def delete(self, category_id: int, session: AsyncSession = None) -> None:
        await self.delete_item(category_id, session)
