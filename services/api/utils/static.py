from fastapi.staticfiles import StaticFiles
from fastapi import Request, HTTPException, status
from fastapi_jwt_auth.exceptions import AuthJWTException
from api.config import AuthJWT
from shared.db import UserTypeEnum


async def verify_auth(request: Request):
    auth = AuthJWT(request)
    try:
        auth.jwt_required()
        auth.get_jwt_subject()
        data = auth.get_jwt_subject().split(',')
        if int(data[1]) != UserTypeEnum.admin:
            raise AuthJWTException()
    except AuthJWTException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )


class AuthStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send) -> None:
        assert scope["type"] == "http"
        await verify_auth(
            Request(scope, receive)
        )
        await super().__call__(scope, receive, send)
