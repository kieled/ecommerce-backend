from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, File, UploadFile, Form
from dependencies import ClientStorage, get_clients
from helpers import album_upload_post

router = APIRouter(
    prefix="/album",
    tags=["album"],
    responses={404: {"description": "Not found"}},
)


class InstagramLink(BaseModel):
    url: str


@router.post("/upload", response_model=InstagramLink, description='Return instagram link to post')
async def album_upload(
        files: List[UploadFile] = File(...),
        caption: str = Form(...),
        clients: ClientStorage = Depends(get_clients)
) -> InstagramLink:
    cl = clients.get()
    media = await album_upload_post(
        cl, files, caption=caption,
        location=cl.location_info(107677462599905))
    return InstagramLink(
        url=f'https://www.instagram.com/p/{media.code}'
    )
