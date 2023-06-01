import strawberry

from api.domains.addresses.types import CustomerAddressInput


@strawberry.input
class CartProductInput:
    product_id: int
    size_id: int | None = None
    color_id: int | None = None
    count: int = 1


@strawberry.input
class CartInput:
    products: list[CartProductInput] | None = strawberry.field(default_factory=list)
    payment_type: int
    address_id: int | None = None
    address: CustomerAddressInput | None = None
    promo: str | None = None


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


__all__ = [
    'CartProductInput',
    'CartInput',
    'CartProductType',
    'CartType',
]
