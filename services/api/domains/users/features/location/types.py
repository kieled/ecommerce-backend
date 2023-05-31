import strawberry


@strawberry.type(name='LocationAddress')
class LocationAddressType:
    road: str = ''
    city: str = ''
    state: str = ''
    country: str = ''
    house_number: str = ''
    postcode: int | None = None


@strawberry.type(name='Location')
class LocationType:
    display_name: str = ''
    address: LocationAddressType = strawberry.field(default_factory=LocationAddressType)


__all__ = [
    'LocationType',
    'LocationAddressType',
]
