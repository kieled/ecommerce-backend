from fastapi import APIRouter, Form, HTTPException, status

from api.domains.users import UsersBL
from api.domains.users.types import SuperUserResponse
from shared.base import settings
from shared.db import User

router = APIRouter()


@router.post('/setup', response_model=SuperUserResponse)
async def setup_router(
        secret_key: str = Form(..., description='Secret key for application'),
        username: str = Form(..., description='Username for admin user account'),
        password: str = Form(..., description='Password for admin user account')
) -> User:
    if secret_key != settings.SECRET_KEY:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid key')
    try:
        return await UsersBL().create_super_user(username, password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
