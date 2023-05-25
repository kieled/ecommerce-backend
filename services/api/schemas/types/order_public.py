from datetime import datetime

import strawberry
from .transactions import PromoType
from ..enums import transaction_status_enum


@strawberry.type(name='OrderPublicProductStock')
class OrderPublicProductStockType:
    id: int = 0
    color: str = ''
    name: str | None = None


@strawberry.type(name='OrderPublicProductSize')
class OrderPublicProductSizeType:
    id: int = 0
    size: str = ''
    name: str | None = None
    product_stock: OrderPublicProductStockType = strawberry.field(default_factory=OrderPublicProductStockType)


@strawberry.type(name='OrderPublicProduct')
class OrderPublicProductType:
    id: int = 0
    title: str = ''
    price: int = 0


@strawberry.type(name='OrderPublicItem')
class OrderPublicItemType:
    id: int = 0
    count: int = 1
    track_code: str | None = None
    product_size: OrderPublicProductSizeType | None = None
    product_stock: OrderPublicProductStockType | None = None
    product: OrderPublicProductType = strawberry.field(default_factory=OrderPublicProductType)


@strawberry.type(name='OrderPublicTransaction')
class OrderPublicTransactionType:
    id: int = 0
    amount: str = ''
    currency: int = 3
    promo: PromoType | None = None
    updated_at: str = str(datetime.now())
    orders: list[OrderPublicItemType] = strawberry.field(default_factory=list)
    status: transaction_status_enum = transaction_status_enum.created


@strawberry.type(name='OrderPublicList')
class OrderPublicListType:
    items: list[OrderPublicTransactionType] = strawberry.field(default_factory=list)
    count: int = 0
