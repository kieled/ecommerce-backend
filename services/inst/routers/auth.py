import json
import logging
from typing import Optional, Dict
from fastapi import APIRouter, Depends, Form
from inst.core import ClientStorage, get_clients

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
        clients: ClientStorage = Depends(get_clients)
) -> str:
    cl = clients.client()

    if locale != "":
        cl.set_locale(locale)

    result = cl.login(
        username,
        password,
        verification_code=verification_code
    )
    if result:
        clients.set(cl)
        return cl.sessionid
    return result


@router.post("/relogin")
async def auth_relogin(
        clients: ClientStorage = Depends(get_clients)
) -> bool:
    cl = clients.get()
    result = cl.relogin()
    return result


@router.get("/settings/get")
async def settings_get(
        clients: ClientStorage = Depends(get_clients)
) -> Dict:
    cl = clients.get()
    return cl.get_settings()


@router.post("/settings/set")
async def settings_set(
        settings: str = Form(...),
        clients: ClientStorage = Depends(get_clients)
) -> str:
    try:
        cl = clients.get()
    except Exception as e:
        logging.info(e.__class__.__name__)
        cl = clients.client()
    cl.set_settings(json.loads(settings))
    cl.expose()
    clients.set(cl)
    return cl.sessionid
