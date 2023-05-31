import strawberry
from .enums import user_type_enum


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


@strawberry.type(name='User')
class UserType:
    id: int
    first_name: str | None = None
    type: user_type_enum = user_type_enum.user
    username: str | None = None
    telegram_chat_id: str | None = None
    temp_user_id: str | None = None


@strawberry.type(name='HashPassword')
class HashPasswordType:
    hash: str


@strawberry.type(name='TelegramUser')
class TelegramUserType:
    username: str | None = None
    first_name: str | None = None


__all__ = [
    'TelegramUserType',
    'UserType',
    'HashPasswordType',
    'CustomerAddressType',
]
