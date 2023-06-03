from fastapi_jwt_auth.exceptions import AuthJWTException
from .config import AuthJWT
from fastapi import Depends


async def get_auth_context(
        auth: AuthJWT = Depends()
):
    try:
        auth.jwt_required()
        user_id = int(auth.get_jwt_subject().split(',')[0])
    except AuthJWTException or ValueError:
        user_id = None

    return {
        'user_id': user_id
    }


__all__ = [
    'get_auth_context',
]
