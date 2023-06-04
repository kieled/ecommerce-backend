import strawberry
from pydantic import BaseModel

from .enums import user_type_enum


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


class SuperUserResponse(BaseModel):
    id: int
    username: str


__all__ = [
    'TelegramUserType',
    'UserType',
    'HashPasswordType',
    'SuperUserResponse',
]
