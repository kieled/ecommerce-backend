import functools
from asyncio import current_task
from contextlib import asynccontextmanager
from typing import TypeVar, Callable, AsyncGenerator
import inspect
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession, async_sessionmaker, create_async_engine

from shared.base import settings

_session = async_sessionmaker(
    create_async_engine(settings.db_url),
    expire_on_commit=False
)


@asynccontextmanager
async def scoped_session() -> AsyncGenerator[AsyncSession, any, None]:
    scoped_factory = async_scoped_session(
        _session,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as s:
            yield s
    finally:
        await scoped_factory.remove()


F = TypeVar('F', bound=Callable)


def session_wrap(f: F) -> F:
    @functools.wraps(f)
    async def decorator(*args, **kwargs):
        if 'session' in kwargs or any(isinstance(arg, AsyncSession) for arg in args):
            return await f(*args, **kwargs)
        async with scoped_session() as s:
            kwargs.update({'session': s})
            return await f(*args, **kwargs)

    if inspect.iscoroutinefunction(f) and 'session' in inspect.signature(f).parameters:
        return decorator
    else:
        return f


ClassType = TypeVar('ClassType', bound=object)


def cls_session(cls: ClassType) -> ClassType:
    for name, method in vars(cls).items():
        setattr(cls, name, session_wrap(method))

    return cls
