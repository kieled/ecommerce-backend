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
