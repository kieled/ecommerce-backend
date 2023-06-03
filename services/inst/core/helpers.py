import aiofiles
import os

from instagrapi import Client


async def album_upload_post(cl: Client, image_paths: list[str], **kwargs):
    async with aiofiles.tempfile.TemporaryDirectory() as d:
        paths = []
        for i in range(len(image_paths)):
            filename, ext = os.path.splitext(image_paths[i])
            async with aiofiles.open(image_paths[i], 'rb') as upload_file:
                async with aiofiles.tempfile.NamedTemporaryFile(suffix=ext, delete=False, dir=d) as f:
                    await f.write(await upload_file.read())
                    paths.append(f.name)
        return cl.album_upload(paths, **kwargs)
