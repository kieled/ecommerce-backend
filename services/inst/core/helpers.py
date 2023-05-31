from aiofiles import tempfile
import os


async def album_upload_post(cl, files, **kwargs):
    async with tempfile.TemporaryDirectory() as d:
        paths = []
        for i in range(len(files)):
            filename, ext = os.path.splitext(files[i].filename)
            async with tempfile.NamedTemporaryFile(suffix=ext, delete=False, dir=d) as f:
                await f.write(await files[i].read())
                paths.append(f.name)
        return cl.album_upload(paths, **kwargs)
