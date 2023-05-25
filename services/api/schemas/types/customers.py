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


@strawberry.type(name='CustomerCard')
class CustomerCardType:
    product_id: int = 0
    size_id: int | None = None
    color_id: int | None = None
    price: str = ''
    size: str | None = None
    image: str = ''
    stock: str = ''
    title: str = ''
    count: int = 0


@strawberry.type(name='CustomerCardList')
class CustomerCardListType:
    items: list[CustomerCardType] = strawberry.field(default_factory=list)
    sum: str = ''
