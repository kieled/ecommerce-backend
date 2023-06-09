import strawberry
from .enums import product_status_enum
from ..features.images import ProductCreateImageInput


@strawberry.input
class ProductColorInput:
    image: str
    sizes: list[str]


@strawberry.input
class ProductUpdateInput:
    product_id: int
    category_id: int | None = None
    title: str | None = None
    description: str | None = None
    status: product_status_enum | None = None
    price: int | None = None
    price_buy: int | None = None
    inst_url: str | None = None


@strawberry.input
class ProductSizeInput:
    size: str
    name: str | None = None


@strawberry.input(name='ProductStockInput')
class ProductStockItemInput:
    color: str
    image: ProductCreateImageInput
    name: str | None = None
    sizes: list[ProductSizeInput] = strawberry.field(default_factory=list)


@strawberry.input
class ProductParamInput:
    name: str
    value: str


@strawberry.input(name='ProductInput')
class ProductCreateInput:
    title: str
    description: str
    url: str
    price_buy: int
    price: int
    category_id: int
    images: list[ProductCreateImageInput] = strawberry.field(default_factory=list)
    stocks: list[ProductStockItemInput] = strawberry.field(default_factory=list)
    params: list[ProductParamInput] = strawberry.field(default_factory=list)


__all__ = [
    'ProductSizeInput',
    'ProductUpdateInput',
    'ProductCreateInput',
    'ProductStockItemInput',
    'ProductColorInput',
    'ProductParamInput',
]
