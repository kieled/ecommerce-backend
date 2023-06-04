import strawberry


@strawberry.input
class CustomerAddressInput:
    flat: int | None = None
    house: str
    street: str
    city: str
    region: str
    country: str
    postal_index: int
    first_name: str
    last_name: str


@strawberry.input
class AddressInput:
    from api.domains.products.features.cart import CartProductInput

    products: list[CartProductInput] | None = strawberry.field(default_factory=list)
    payment_type: int
    address_id: int | None = None
    address: CustomerAddressInput | None = None
    promo: str | None = None


__all__ = [
    'CustomerAddressInput',
    'AddressInput',
]
