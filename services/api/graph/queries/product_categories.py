import strawberry
from config import session
from schemas import ProductCategoryType
from services import ProductCategoryService
from utils import orm_to_strawberry


@strawberry.type
class ProductCategoryQuery:
    @strawberry.field(
        description='Product categories list'
    )
    async def product_categories(self, info) -> list[ProductCategoryType]:
        """ Get product categories """
        async with session() as s:
            data = await ProductCategoryService(s, info).list()

        prepared_data = orm_to_strawberry(data, ProductCategoryType)

        return prepared_data
