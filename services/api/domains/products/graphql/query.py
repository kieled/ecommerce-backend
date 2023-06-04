import strawberry
from alchemy_graph import orm_to_strawberry
from strawberry.types import Info

from ..bl import ProductBL
from ..features.aliexpress_parser import ProductParsedType, aliexpress_parser
from api.domains.products.features.cart import CartProductInput, CartType, cart_products
from api.utils.graphql import IsAdmin
from ..types import ProductListType, ProductItemType, ProductDetailType, PublicListType, PublicDetailType


class ProductQuery:
    @strawberry.field(description='Customer cart products with total sum')
    async def customer_cart(self, products: list[CartProductInput]) -> CartType:
        return await cart_products(products)

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
        data = await ProductBL(info, page).list(search, category_id)

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
        data = await ProductBL(info).detail(product_id)
        return orm_to_strawberry(data, ProductDetailType)

    @strawberry.field(
        permission_classes=[IsAdmin],
        description='Parse product info'
    )
    async def fetch_product(self, url: str) -> ProductParsedType:
        """ Parse product info from aliexpress_parser """
        return await aliexpress_parser(url)

    @strawberry.field
    async def products_public(
            self,
            info: Info,
            page: int | None = 1,
            category_id: int | None = None
    ) -> PublicListType:
        """ Public products list """
        data = await ProductBL(info, page=page).public_list(category_id)
        for i, product in enumerate(data.items):
            product.images = data.items[i].images[:1]
        return orm_to_strawberry(data, PublicListType)

    @strawberry.field
    async def public_detail(self, info, product_id: int) -> PublicDetailType:
        """ Public product detail """
        data = await ProductBL(info).detail(product_id)
        return orm_to_strawberry(data, PublicDetailType)
