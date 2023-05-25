import functools
from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_scoped_session

from .config import session


@asynccontextmanager
async def scoped_session():
    scoped_factory = async_scoped_session(
        session,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as s:
            yield s
    finally:
        await scoped_factory.remove()


def session_wrap(f):
    @functools.wraps(f)
    async def decorator(*args, **kwargs):
        async with scoped_session() as s:
            kwargs.update({'session': s})
            return await f(*args, **kwargs)

    return decorator
