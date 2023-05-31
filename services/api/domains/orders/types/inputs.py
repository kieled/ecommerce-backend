import strawberry
from api.domains.addresses.types import CustomerAddressInput


@strawberry.input
class UpdateOrderInput:
    order_id: int
    order_url: str | None = None
    track_code: str | None = None


@strawberry.input
class CreateOrderProductInput:
    product_id: int
    size_id: int | None = None
    color_id: int | None = None
    count: int = 1


@strawberry.input
class CreateOrderInput:
    products: list[CreateOrderProductInput] | None = strawberry.field(default_factory=list)
    payment_type: int
    address_id: int | None = None
    address: CustomerAddressInput | None = None
    promo: str | None = None


__all__ = [
    'CreateOrderProductInput',
    'CreateOrderInput',
    'UpdateOrderInput',
]
