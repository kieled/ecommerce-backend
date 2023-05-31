import io
import os
import zipfile
from io import BytesIO
import requests
from math import floor
from PIL import Image

from .types import ProductCreateImageInput
from shared.db import ImageCropDirectionEnum


def crop_image(image: Image, side: ImageCropDirectionEnum, percent: int) -> Image:
    sizes = image.size
    crop_size = [0, 0, sizes[0], sizes[1]]
    pixels_to_crop = floor(sizes[1] * (percent / 100))
    if side == ImageCropDirectionEnum.top:
        crop_size[1] += pixels_to_crop
    else:
        crop_size[3] -= pixels_to_crop
    image = image.crop(crop_size)
    return image


def center_image(image: Image) -> Image:
    if image.size[0] != image.size[1]:
        size_max = max(image.size)
        new_im = Image.new('RGB', (size_max, size_max), (255, 255, 255))
        x_offset = int((size_max - image.size[0]) / 2)
        y_offset = int((size_max - image.size[1]) / 2)
        new_im.paste(image, (x_offset, y_offset))
        return new_im
    return image


def stamp_watermark(image: Image) -> Image:
    logo = Image.open('/assets/watermark.png')

    image.paste(logo, (0, int(image.height / 2 - logo.height / 2)), logo)
    return image


def get_image_path(product_id: int, folder: str, name: str):
    path = os.path.join(os.getcwd(), f'/assets/aliexpress_parser/{product_id}/')
    end_path = os.path.join(path, folder)
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(end_path):
        os.mkdir(end_path)

    files = os.listdir(end_path)
    filename = str(len(files) + 1) if not name else name
    return os.path.join(end_path, f'{filename}.webp')


async def handle_image(
        product_id: int,
        input_img: ProductCreateImageInput,
        session,
        folder: str = 'default',
        filename: str | None = None,
) -> str:
    if input_img.file:
        path = f'/assets{input_img.file}'
        image = Image.open(path)
    else:
        async with session.get(input_img.url) as r:
            image = Image.open(BytesIO(await r.read()))
    if input_img.crop_direction is not None:
        image = crop_image(image, input_img.crop_direction, input_img.crop_percent)
    image = center_image(image)
    image = stamp_watermark(image)

    image_path = get_image_path(product_id, folder, filename)
    image.save(image_path)
    result = '/images/' + image_path[image_path.index('aliexpress_parser/') + 11:]
    return result


def download_images(
        images: list[str]
):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as file:
        with requests.Session() as s:
            for i, image in enumerate(images):
                img = s.get(image)
                img_file = BytesIO(img.content)
                file.writestr(f'{i}.jpg', img_file.getvalue())
    zip_buffer.seek(0)
    return zip_buffer


def get_local_images(product_id: int):
    def get_folder_list(folder: str, folder_path: str):
        return [f'{folder_path}/{folder}/{name}' for name in os.listdir(f'{folder_path}/{folder}')]

    def get_zip_path(full_path: str):
        return full_path.split(f'/assets/aliexpress_parser/{product_id}/')[1]

    root_path = f'/assets/aliexpress_parser/{product_id}'
    colors_images = get_folder_list('colors', root_path)
    default_images = get_folder_list('default', root_path)
    all_images = [*colors_images, *default_images]
    result = [{'zip': get_zip_path(image), 'path': image} for image in all_images]

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as file:
        for item in result:
            file.write(item['path'], item['zip'])
    return zip_buffer.getvalue()


__all__ = [
    'handle_image',
    'get_local_images',
    'download_images',
]
