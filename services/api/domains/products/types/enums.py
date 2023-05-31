import strawberry

from shared.db import ProductStatusEnum

product_status_enum = strawberry.enum(ProductStatusEnum)

__all__ = [
    'product_status_enum',
]
