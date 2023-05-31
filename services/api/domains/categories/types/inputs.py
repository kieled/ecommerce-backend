import strawberry


@strawberry.input
class ProductCategoryInput:
    name: str
    slug: str


@strawberry.input
class UpdateProductCategoryInput:
    id: int
    name: str | None = None
    slug: str | None = None


__all__ = [
    'UpdateProductCategoryInput',
    'ProductCategoryInput',
]
