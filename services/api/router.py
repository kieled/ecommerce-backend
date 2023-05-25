import os
import uuid
from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from shared.schemas import MessageSchema
from utils import download_images, get_local_images
from api.config import rabbit_connection

router = APIRouter()


class ImagesSchema(BaseModel):
    images: list[str]


@router.post('/load-images')
async def load_images(data: ImagesSchema):
    headers = {"Content-Disposition": "attachment; filename=images.zip"}
    return StreamingResponse(download_images(data.images), status_code=200, media_type='application/zip',
                             headers=headers)


@router.get('/download/{product_id}')
async def product_images(product_id: int):
    zip_buffer = get_local_images(product_id)
    return StreamingResponse(iter([zip_buffer]), media_type='application/x-zip-compressed',
                             headers={"Content-Disposition": f"attachment; filename=images.zip"})


@router.post('/upload-files/')
async def create_temp_images(files: list[UploadFile]):
    file_names = []
    for file in files:
        file_name = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        path = os.path.join(os.getcwd(), f'assets/temp/{file_name}')
        with open(path, "wb") as buffer:
            buffer.write(await file.read())
        file_names.append(f'/temp/{file_name}')
        await rabbit_connection.send_messages(MessageSchema(action='image:delete', body={
            'path': path
        }), delay=60 * 60)
    return {"files": file_names}
