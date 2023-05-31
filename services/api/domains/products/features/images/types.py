import strawberry
from pydantic import BaseModel

from shared.db import ImageCropDirectionEnum

image_crop_direction_enum = strawberry.enum(ImageCropDirectionEnum)


@strawberry.input
class ProductCreateImageInput:
    url: str | None = None
    file: str | None = None
    crop_direction: image_crop_direction_enum | None = None
    crop_percent: int | None = None


class ImagesSchema(BaseModel):
    images: list[str]


__all__ = [
    'ProductCreateImageInput',
    'ImagesSchema',
]
