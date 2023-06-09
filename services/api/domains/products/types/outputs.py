import strawberry
from .enums import product_status_enum
from api.domains.categories.types import ProductCategoryType, PublicCategoryType


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


@strawberry.type(name='PublicParamItem')
class PublicParamItemType:
    id: int
    name: str = ''
    value: str = ''


@strawberry.type(name='PublicImage')
class PublicImageType:
    id: int
    path: str = ''


@strawberry.type(name='PublicSize')
class PublicSizeType:
    id: int
    size: str = ''
    name: str | None = None


@strawberry.type(name='PublicStockItem')
class PublicStockItemType:
    id: int
    image: str = ''
    color: str = ''
    name: str | None = None
    sizes: list[PublicSizeType] = strawberry.field(default_factory=list)


@strawberry.type(name='PublicItem')
class PublicItemType:
    id: int
    title: str = ''
    price: str = ''
    images: list[PublicImageType] = strawberry.field(default_factory=list)


@strawberry.type(name='PublicDetail')
class PublicDetailType:
    id: int
    title: str = ''
    price: str = ''
    description: str = ''

    category: PublicCategoryType = strawberry.field(default=PublicCategoryType)
    images: list[PublicImageType] = strawberry.field(default_factory=list)
    stocks: list[PublicStockItemType] = strawberry.field(default_factory=list)
    params: list[PublicParamItemType] = strawberry.field(default_factory=list)


@strawberry.type(name='PublicList')
class PublicListType:
    items: list[PublicItemType] = strawberry.field(default_factory=list)
    count: int = 0


__all__ = [
    'ProductParamType',
    'ProductStockType',
    'ProductItemType',
    'ProductSizeType',
    'ProductDetailType',
    'CreatedProductType',
    'ProductListType',
    'ProductImageType',
    'CreatedProductImageType',
    'PublicListType',
    'PublicDetailType',
    'PublicItemType',
    'PublicSizeType',
    'PublicParamItemType',
    'PublicStockItemType',
    'PublicImageType',
]
