from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, async_scoped_session
from sqlalchemy.orm import declarative_base

from shared.base import settings

engine = create_async_engine(settings.db_url)

session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    expire_on_commit=False
)

Base = declarative_base()
