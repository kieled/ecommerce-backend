import strawberry
from alchemy_graph import orm_to_strawberry, strawberry_to_dict

from ..types import ProductCategoryInput, UpdateProductCategoryInput, ProductCategoryType
from ..bl import ProductCategoryBL
from api.domains.users.features.auth import IsAdmin


@strawberry.type
class ProductCategoryMutation:
    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Update product category'
    )
    async def update_product_category(self, payload: UpdateProductCategoryInput, info) -> ProductCategoryType:
        await ProductCategoryBL(info).update(payload)
        return ProductCategoryType(**strawberry_to_dict(payload))

    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Create product category'
    )
    async def create_product_category(self, payload: ProductCategoryInput, info) -> ProductCategoryType:
        data = await ProductCategoryBL(info).create(payload)
        return orm_to_strawberry(data, ProductCategoryType)

    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Delete product category'
    )
    async def delete_product_category(self, category_id: int, info) -> None:
        await ProductCategoryBL(info).delete(category_id)
