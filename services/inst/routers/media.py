from fastapi import APIRouter, Depends, Form

from dependencies import ClientStorage, get_clients

router = APIRouter(
    prefix="/media",
    tags=["media"],
    responses={404: {"description": "Not found"}}
)


@router.post("/edit")
async def media_edit(
        instagram_url: str = Form(...),
        caption: str = Form(...),
        clients: ClientStorage = Depends(get_clients)
) -> None:
    cl = clients.get()
    media_pk = cl.media_pk_from_url(instagram_url)
    media_id = cl.media_id(media_pk)
    cl.media_edit(
        media_id,
        caption,
        location=cl.location_info(107677462599905)
    )
