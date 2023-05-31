import base64
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from shared.base import settings


class Settings(BaseModel):
    authjwt_token_location: set = {'cookies'}
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_secret_key: str = base64.b64decode(
        settings.SECRET_KEY).decode('utf-8')
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return Settings()


__all__ = [
    'AuthJWT'
]
