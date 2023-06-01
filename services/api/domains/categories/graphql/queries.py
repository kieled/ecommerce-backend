import strawberry
from alchemy_graph import orm_to_strawberry
from ..types import ProductCategoryType
from ..bl import ProductCategoryBL


@strawberry.type
class ProductCategoryQuery:
    @strawberry.field(
        description='Product categories list'
    )
    async def product_categories(self, info) -> list[ProductCategoryType]:
        """ Get product categories """
        data = await ProductCategoryBL(info).list()
        return orm_to_strawberry(data, ProductCategoryType)
