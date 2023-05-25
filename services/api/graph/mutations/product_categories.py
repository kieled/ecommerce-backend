import strawberry
from config import session
from schemas import ProductCategoryInput, UpdateProductCategoryInput, ProductCategoryType
from services import ProductCategoryService
from utils import IsAdmin


@strawberry.type
class ProductCategoryMutation:
    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Update product category'
    )
    async def update_product_category(self, payload: UpdateProductCategoryInput, info) -> ProductCategoryType:
        async with session() as s:
            data = await ProductCategoryService(s, info).update(payload)
        return ProductCategoryType(**data)

    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Create product category'
    )
    async def create_product_category(self, payload: ProductCategoryInput, info) -> ProductCategoryType:
        async with session() as s:
            data = await ProductCategoryService(s, info).create(payload)
        return ProductCategoryType(**data)

    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Delete product category'
    )
    async def delete_product_category(self, category_id: int, info) -> None:
        async with session() as s:
            await ProductCategoryService(s, info).delete(category_id)
