import functools
from asyncio import current_task
from contextlib import asynccontextmanager
from typing import TypeVar, Callable
import inspect

from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession

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


T = TypeVar('T', bound=Callable)


def session_wrap(f: T) -> T:
    @functools.wraps(f)
    async def decorator(*args, **kwargs):
        if 'session' in kwargs or [i for i in args if isinstance(i, AsyncSession)]:
            return await f(*args, **kwargs)
        async with scoped_session() as s:
            kwargs.update({'session': s})
            return await f(*args, **kwargs)

    if 'session' in inspect.signature(f).parameters:
        return decorator
    else:
        return f


ClassType = TypeVar('ClassType')


def cls_session(cls: ClassType) -> ClassType:
    for name, method in vars(cls).items():
        if inspect.iscoroutinefunction(method) \
                and 'session' in inspect.signature(method).parameters:
            setattr(cls, name, session_wrap(method))

    return cls
