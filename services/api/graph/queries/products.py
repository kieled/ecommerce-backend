import strawberry
from config import session
from schemas import ProductListType, ProductDetailType, ProductParsedType, ProductItemType, CurrentPricesType
from services import ProductService
from utils import IsAdmin, orm_to_strawberry
from parsers import prices_manager, aliexpress_parser


@strawberry.type
class ProductQuery:
    @strawberry.field(
        permission_classes=[IsAdmin],
        description='List of all products'
    )
    async def products(
            self,
            info,
            page: int | None = 1,
            search: int | None = None,
            category_id: int | None = None
    ) -> ProductListType:
        """ Products list """
        async with session() as s:
            data = await ProductService(s, info, page).list(search, category_id)

        products: list[ProductItemType] = orm_to_strawberry(data.items, ProductItemType)

        if len(products) and isinstance(products[0].images, list):
            for i, product in enumerate(products):
                products[i].images = products[i].images[:1]

        return ProductListType(
            count=data.count,
            products=products
        )

    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Product detail info'
    )
    async def product_detail(self, product_id: int, info) -> ProductDetailType:
        """ Product detail """
        async with session() as s:
            data = await ProductService(s, info).detail(product_id)
        return orm_to_strawberry(data, ProductDetailType)

    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Parse product info'
    )
    async def fetch_product(self, url: str) -> ProductParsedType:
        """ Parse product info from aliexpress """
        return await aliexpress_parser(url)

    @strawberry.field(
        description='Get current price from BYN to RUB and USD'
    )
    async def currency_prices(self) -> CurrentPricesType:
        return CurrentPricesType(
            **(await prices_manager.get())
        )
