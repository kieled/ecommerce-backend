import tempfile
from PIL import Image
import os
from io import BytesIO


async def album_upload_post(cl, files, **kwargs):
    with tempfile.TemporaryDirectory() as td:
        paths = []
        for i in range(len(files)):
            filename, ext = os.path.splitext(files[i].filename)
            fp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False, dir=td)
            if ext == ".webp":
                with Image.open(BytesIO(await files[i].read())) as img:
                    img.save(fp.name, "JPEG")
            else:
                fp.write(await files[i].read())
            fp.close()
            paths.append(fp.name)
        return cl.album_upload(paths, **kwargs)
