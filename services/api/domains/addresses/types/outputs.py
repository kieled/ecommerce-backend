import strawberry


@strawberry.type(name='CustomerAddress')
class CustomerAddressType:
    id: int
    flat: int | None = None
    house: str = ''
    street: str = ''
    city: str = ''
    region: str = ''
    country: str = ''
    postal_index: int = 0
    first_name: str = ''
    last_name: str = ''


__all__ = [
    'CustomerAddressType',
]
