import strawberry


@strawberry.type(name='Cart')
class CartProductType:
    product_id: int = 0
    size_id: int | None = None
    color_id: int | None = None
    price: str = ''
    size: str | None = None
    image: str = ''
    stock: str = ''
    title: str = ''
    count: int = 0


@strawberry.type(name='CartItems')
class CartType:
    items: list[CartProductType] = strawberry.field(default_factory=list)
    sum: int = 0


@strawberry.input
class CartProductInput:
    product_id: int
    size_id: int | None = None
    color_id: int | None = None
    count: int = 1


__all__ = [
    'CartProductType',
    'CartType',
    'CartProductInput',
]
