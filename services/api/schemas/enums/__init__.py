import strawberry
from shared.db import ProductStatusEnum, ImageCropDirectionEnum, CurrencyEnum, UserTypeEnum, TransactionStatusEnum

product_status_enum = strawberry.enum(ProductStatusEnum)
image_crop_direction_enum = strawberry.enum(ImageCropDirectionEnum)
currency_enum = strawberry.enum(CurrencyEnum)
transaction_status_enum = strawberry.enum(TransactionStatusEnum)
user_type_enum = strawberry.enum(UserTypeEnum)

__all__ = [
    'product_status_enum',
    'transaction_status_enum',
    'user_type_enum',
    'currency_enum',
    'image_crop_direction_enum'
]
