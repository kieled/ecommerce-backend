import json
from typing import Optional
from fastapi import APIRouter, Form, Depends, HTTPException, status
from pydantic import BaseModel

from inst.core import client_storage, get_clients
from inst.core.storage import ClientStorage

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)


class SessionResponse(BaseModel):
    success: bool
    session_id: str | None


@router.post("/login", response_model=SessionResponse)
async def auth_login(
        username: str = Form(...),
        password: str = Form(...),
        verification_code: Optional[str] = Form(""),
        locale: Optional[str] = Form(""),
        client: ClientStorage = Depends(get_clients)
) -> SessionResponse:
    cl = client.cl
    if locale != "":
        cl.set_locale(locale)

    result = cl.login(
        username,
        password,
        verification_code=verification_code
    )
    if result:
        client_storage.set(cl)
        return SessionResponse(success=True, session_id=cl.sessionid)
    return SessionResponse(success=False)


@router.post("/relogin", response_model=SessionResponse)
async def auth_relogin(
        storage: ClientStorage = Depends(get_clients)
) -> SessionResponse:
    return SessionResponse(success=storage.cl.relogin())


@router.get("/settings/get")
async def settings_get(
        storage: ClientStorage = Depends(get_clients)
) -> dict:
    return storage.cl.get_settings()


@router.post("/settings/set", response_model=SessionResponse)
async def settings_set(
        settings: str = Form(...),
        storage: ClientStorage = Depends(get_clients)
) -> SessionResponse:
    try:
        data = json.loads(settings)
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid / unparsable format')
    storage.cl.set_settings(data)
    storage.cl.expose()
    await storage.set()
    return SessionResponse(success=True, session_id=storage.cl.sessionid)
