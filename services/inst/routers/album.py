from fastapi import APIRouter, Depends, Form
from instagrapi import Client

from inst.core import get_clients, album_upload_post
from inst.schemas import InstagramLink

router = APIRouter(
    prefix="/album",
    tags=["album"],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload", response_model=InstagramLink, description='Return instagram link to post')
async def album_upload(
        images: list[str] = Form(...),
        caption: str = Form(...),
        client: Client = Depends(get_clients)
) -> InstagramLink:
    media = await album_upload_post(client, images, caption=caption)
    return InstagramLink(
        url=f'https://www.instagram.com/p/{media.code}'
    )
