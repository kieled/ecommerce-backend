from consumer.services import MigrationService
from shared.db import scoped_session


async def migration(temp: str, user_id: int):
    if temp is None or user_id is None:
        return
    async with scoped_session() as s:
        await MigrationService(s).from_temp(temp, user_id)


__all__ = ['migration']
