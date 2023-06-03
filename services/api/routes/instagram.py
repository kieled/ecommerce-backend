import aiohttp
from fastapi import APIRouter, Form, Depends

from api.utils.routes import check_admin

router = APIRouter()


@router.post('/auth')
async def instagram_authentication(
        username: str = Form(...),
        password: str = Form(...),
        verification_code: str | None = Form(""),
        locale: str | None = Form(""),
        _: bool = Depends(check_admin)
):
    async with aiohttp.ClientSession() as s:
        async with s.post('http://inst:8000/login', data=dict(
                username=username,
                password=password,
                verification_code=verification_code,
                locale=locale
        )) as res:
            return await res.json()
