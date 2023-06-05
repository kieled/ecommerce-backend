from .storage import client_storage


async def get_clients():
    async with client_storage as c:
        yield c
