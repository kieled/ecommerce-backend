from api.config import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from strawberry import BasePermission
from strawberry.types import Info
from shared.db import UserTypeEnum
from fastapi import Request


class IsAdmin(BasePermission):
    message = "Access denied"

    async def has_permission(self, source: any, info: Info, **kwargs) -> bool:
        request: Request = info.context["request"]
        auth = AuthJWT(req=request)
        try:
            auth.jwt_required()
            data = auth.get_jwt_subject().split(',')
            if int(data[1]) == UserTypeEnum.admin:
                return True
            return False
        except AuthJWTException:
            return False


class IsAuthenticated(BasePermission):
    message = 'Not authenticated'

    async def has_permission(self, source: any, info: Info, **kwargs) -> bool:
        temp_user_id = info.context.get('request').cookies.get('tempId')
        user_id = info.context.get('user_id')

        if temp_user_id or user_id:
            return True
        return False
