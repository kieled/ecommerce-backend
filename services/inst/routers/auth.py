import json
from typing import Optional
from fastapi import APIRouter, Form
from inst.core import client_storage

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)


@router.post("/login")
async def auth_login(
        username: str = Form(...),
        password: str = Form(...),
        verification_code: Optional[str] = Form(""),
        locale: Optional[str] = Form(""),
) -> str:
    with client_storage as cl:
        if locale != "":
            cl.set_locale(locale)

        result = cl.login(
            username,
            password,
            verification_code=verification_code
        )
        if result:
            client_storage.set(cl)
            return cl.sessionid
    return result


@router.post("/relogin")
async def auth_relogin() -> bool:
    with client_storage as cl:
        return cl.relogin()


@router.get("/settings/get")
async def settings_get() -> dict:
    with client_storage as cl:
        return cl.get_settings()


@router.post("/settings/set")
async def settings_set(
        settings: str = Form(...),
) -> dict[str, str]:
    try:
        data = json.loads(settings)
    except json.JSONDecodeError:
        return {'error': 'Invalid / unparsable format'}
    client_storage.set()
    with client_storage as cl:
        cl.set_settings(data)
        cl.expose()
        client_storage.set(cl.get_settings())
        return cl.sessionid
