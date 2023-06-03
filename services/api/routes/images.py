import os
import uuid
import aiofiles

from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import StreamingResponse
from starlette.staticfiles import StaticFiles

from api.broker import rabbit_connection
from api.domains.products.features.images import download_images, get_local_images, ImagesSchema
from api.utils.routes import check_admin
from shared.schemas import MessageSchema

router = APIRouter()

# Paths for sharing images
router.mount('/images', StaticFiles(directory="assets/aliexpress"), name="images")
router.mount('/temp', StaticFiles(directory="assets/temporary"), name="temp_images")


@router.post('/load-images')
async def load_images(data: ImagesSchema, _: bool = Depends(check_admin)):
    headers = {"Content-Disposition": "attachment; filename=images.zip"}
    return StreamingResponse(await download_images(data.images), status_code=200, media_type='application/zip',
                             headers=headers)


@router.get('/download/{product_id}')
async def product_images(product_id: int, _: bool = Depends(check_admin)):
    zip_buffer = get_local_images(product_id)
    return StreamingResponse(iter([zip_buffer]), media_type='application/x-zip-compressed',
                             headers={"Content-Disposition": f"attachment; filename=images.zip"})


@router.post('/upload-files/')
async def create_temp_images(files: list[UploadFile], _: bool = Depends(check_admin)):
    file_names = []
    for file in files:
        file_name = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        path = f'/assets/temporary/{file_name}'
        async with aiofiles.open(path, "wb") as buffer:
            await buffer.write(await file.read())
        file_names.append(f'/temp/{file_name}')
        await rabbit_connection.send_messages(MessageSchema(action='image:delete', body={
            'path': path
        }), delay=60 * 60)
    return {"files": file_names}
