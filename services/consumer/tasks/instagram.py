from consumer.services import InstagramService


async def add(data: dict):
    await InstagramService(data).add_post()


async def edit(data: dict):
    await InstagramService(data).edit_post()


__all__ = ['add', 'edit']
