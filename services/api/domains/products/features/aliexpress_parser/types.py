import strawberry


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


__all__ = [
    'ProductParsedParamsType',
    'ProductParsedType',
    'ProductParsedColorType',
]
