import strawberry

from shared.db import UserTypeEnum

user_type_enum = strawberry.enum(UserTypeEnum)

__all__ = [
    'user_type_enum',
]
