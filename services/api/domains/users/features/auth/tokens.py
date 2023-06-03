from datetime import timedelta

from shared.db import User
from .config import AuthJWT
from shared.base import settings

ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


def get_tokens(auth: AuthJWT, user: User) -> tuple[str, str]:
    access = auth.create_access_token(
        subject=f'{user.id},{user.type}', expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    refresh = auth.create_refresh_token(
        subject=f'{user.id},{user.type}', expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))
    return access, refresh


def assign_response(auth: AuthJWT, access: str, refresh: str) -> None:
    auth.set_access_cookies(access, max_age=ACCESS_TOKEN_EXPIRES_IN * 60)
    auth.set_refresh_cookies(refresh, max_age=REFRESH_TOKEN_EXPIRES_IN * 60)


__all__ = [
    'get_tokens',
    'assign_response'
]
