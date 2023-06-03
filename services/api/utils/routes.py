from fastapi import Request, HTTPException, status
from fastapi_jwt_auth.exceptions import AuthJWTException

from api.domains.users.features.auth import AuthJWT
from shared.db import UserTypeEnum

AuthException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': 'UNAUTHORIZED'})


def check_admin(request: Request):
    auth = AuthJWT(req=request)
    try:
        auth.jwt_required()
        data = auth.get_jwt_subject().split(',')
        if int(data[1]) == UserTypeEnum.admin:
            return True
        raise AuthException
    except AuthJWTException:
        raise AuthException
