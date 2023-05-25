import strawberry
from ..enums import product_status_enum


@strawberry.type(name='ProductImage')
class ProductImageType:
    id: int
    path: str = ''


@strawberry.type(name='ProductSize')
class ProductSizeType:
    id: int
    size: str = ''
    name: str | None = None


@strawberry.type(name='ProductStock')
class ProductStockType:
    id: int
    name: str | None = None
    color: str = ''
    image: str = ''
    sizes: list[ProductSizeType] = strawberry.field(default_factory=list)


@strawberry.type(name='ProductParamItem')
class ProductParamType:
    id: int
    name: str = ''
    value: str = ''


@strawberry.type(name='ProductItem')
class ProductItemType:
    id: int
    title: str = ''
    description: str = ''
    price_buy: int = 0
    price: int = 0
    status: product_status_enum = product_status_enum.created
    images: list[ProductImageType] = strawberry.field(default_factory=list)


@strawberry.type(name='ProductList')
class ProductListType:
    products: list[ProductItemType] = strawberry.field(default_factory=list)
    count: int = 0


@strawberry.type(name='ProductCategory')
class ProductCategoryType:
    id: int = 0
    slug: str = ''
    name: str = ''


@strawberry.type(name='ProductDetail')
class ProductDetailType:
    id: int
    title: str = ''
    description: str = ''
    price_buy: int = 0
    price: int = 0
    status: product_status_enum = product_status_enum.created
    images: list[ProductImageType] = strawberry.field(default_factory=list)
    ali_url: str = ''
    inst_url: str | None = None
    category: ProductCategoryType = strawberry.field(default_factory=ProductCategoryType)
    stocks: list[ProductStockType] = strawberry.field(default_factory=list)
    params: list[ProductParamType] = strawberry.field(default_factory=list)


@strawberry.type
class CreatedProductImageType:
    id: int = 0
    path: str = ''


@strawberry.type
class CreatedProductType:
    id: int = 0
    images: list[CreatedProductImageType] = strawberry.field(default_factory=list)


@strawberry.type
class ProductParsedColorType:
    name: str
    image: str
    sizes: list[str]


@strawberry.type
class ProductParsedParamsType:
    name: str
    value: str


@strawberry.type
class ProductParsedType:
    url: str
    images: list[str]
    colors: list[ProductParsedColorType]
    params: list[ProductParsedParamsType]


@strawberry.type(name='CurrentPrices')
class CurrentPricesType:
    usd: float = 0
    rub: float = 0
