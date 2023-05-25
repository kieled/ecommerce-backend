from datetime import datetime

import strawberry
from ..enums import transaction_status_enum, user_type_enum


@strawberry.type(name='OrderRequisiteType')
class OrderTypeRequisiteType:
    id: int = 0
    name: str = ''
    detail: str = ''


@strawberry.type(name='OrderRequisite')
class OrderRequisiteType:
    id: int = 0
    info: str = ''
    detail: str = ''
    type: OrderTypeRequisiteType = strawberry.field(default_factory=OrderTypeRequisiteType)


@strawberry.type(name='OrderCustomer')
class OrderCustomerType:
    id: int
    image_url: str | None = None
    first_name: str | None = None
    type: user_type_enum = user_type_enum.user
    telegram_chat_id: str | None = None
    username: str | None = None


@strawberry.type(name='OrderAddress')
class OrderAddressType:
    id: int = 0
    flat: int | None = None
    house: str = ''
    street: str = ''
    region: str = ''
    city: str = ''
    postal_index: int = 0
    first_name: str = ''
    last_name: str = ''
    country: str = ''

    user: OrderCustomerType | None = None
    temp_user_id: int | None = None


@strawberry.type(name='OrderProductCategory')
class OrderProductCategoryType:
    id: int = 0
    name: str = ''


@strawberry.type(name='OrderProduct')
class OrderProductType:
    id: int = 0
    title: str = ''
    price_buy: int = 0
    price: int = 0
    aliUrl: str = ''
    category: OrderProductCategoryType = strawberry.field(default_factory=OrderProductCategoryType)


@strawberry.type(name='OrderProductStock')
class OrderProductStockType:
    id: int = 0
    color: str = ''
    name: str | None = None


@strawberry.type(name='OrderProductSize')
class OrderProductSizeType:
    id: int = 0
    size: str = ''
    name: str | None = None
    product_stock: OrderProductStockType | None = None


@strawberry.type(name='OrderPromo')
class OrderPromoType:
    id: int = 0
    discount: float = 0.0
    code: str = ''


@strawberry.type(name='OrderTransaction')
class OrderTransactionType:
    id: int = 0
    amount: int = 0
    updated_at: str = str(datetime.now())
    status: transaction_status_enum = transaction_status_enum.created
    user_id: int | None = None
    temp_user_id: str | None = None
    bank_number_id: str | None = None
    promo: OrderPromoType | None = None
    requisite: OrderRequisiteType = strawberry.field(default_factory=OrderRequisiteType)


@strawberry.type(name='OrderItem')
class OrderItemType:
    id: int = 0
    order_url: str | None = None
    track_code: str | None = None
    customer_address: OrderAddressType = strawberry.field(default_factory=OrderAddressType)
    product_size: OrderProductSizeType = strawberry.field(default_factory=OrderProductSizeType)
    product_stock: OrderProductStockType | None = None
    count: int = 1
    product: OrderProductType = strawberry.field(default_factory=OrderProductType)
    transaction: OrderTransactionType = strawberry.field(default_factory=OrderTransactionType)


@strawberry.type(name='OrderList')
class OrderListType:
    items: list[OrderItemType] = strawberry.field(default_factory=list)
    count: int = 0


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


@strawberry.type(name='CreatedOrderId')
class CreatedOrderIdType:
    id: int


@strawberry.type(name='PromoStatus')
class PromoResponseType:
    status: bool
    discount: float | None = None
