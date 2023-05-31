import os
from dataclasses import dataclass
import aiohttp
from sqlalchemy import update
from shared.db import Product, scoped_session
from shared.localizations.instagram import description
from shared.schemas import DescriptionSchema


@dataclass
class InstagramService:
    data: dict | None = None

    async def add_post(self):
        images_path = f'/assets/aliexpress/{self.data.get("id")}/default'
        images = os.listdir(images_path)
        images.sort()
        path_images = [os.path.join(images_path, image) for image in images]
        async with aiohttp.ClientSession() as s:
            async with s.post(
                    'http://instagram:8000/album/upload',
                    data={
                        'caption': self._description(),
                        'images': path_images
                    }
            ) as resp:
                json_data = await resp.json()
                instagram_url = json_data['url']
        async with scoped_session() as s:
            sql = update(Product).values(
                inst_url=instagram_url,
            ).where(Product.id == self.data.get('id'))
            await s.execute(sql)
            await s.commit()

    async def edit_post(self):
        caption = self._description()
        async with aiohttp.ClientSession() as s:
            async with s.post(
                    'http://instagram:8000/media/edit',
                    data=dict(
                        instagram_url=self.data.get('inst_url'),
                        caption=caption
                    )
            ) as r:
                await r.text()

    def _description(self):
        sizes = max(
            self.data.get('stocks'),
            key=lambda x: len(x.get('sizes'))
        ).get('sizes')
        return description(DescriptionSchema(
            id=self.data.get('id'),
            title=self.data.get('title'),
            description=self.data.get('description'),
            price=self.data.get('price'),
            materials=self.data.get('params'),
            sizes=sizes
        ))
