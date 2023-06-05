import os
from dataclasses import dataclass

from instagrapi import Client
import json
import aiofiles


@dataclass
class DB:
    path: str

    async def update(self, data: dict) -> None:
        async with aiofiles.open(self.path, 'wb') as f:
            await f.write(json.dumps(data).encode())

    async def load(self) -> dict | None:
        if not os.path.isfile(self.path):
            return None
        async with aiofiles.open(self.path, 'rb') as f:
            return json.loads((await f.read()).decode())


class ClientStorage:
    db = DB('./db.json')
    cl: Client

    async def set(self):
        await self.db.update(self.cl.get_settings())

    async def __aenter__(self):
        self.cl = Client(
            settings=await self.db.load(),
            request_timeout=0.5
        )
        return self


client_storage = ClientStorage()
