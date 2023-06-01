from typing import Sequence, TypeVar, Generic, Callable, Optional, TypeAlias
from alchemy_graph import get_only_selected_fields
from pydantic.generics import GenericModel
from sqlalchemy import desc, delete, insert, update, select, func, Select, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from strawberry.types import Info

T = TypeVar('T', bound=DeclarativeMeta)
FilterType: TypeAlias = list[ColumnElement] | tuple[ColumnElement] | bool | any | None


class ListType(GenericModel, Generic[T]):
    items: Sequence[T]
    count: int


def get_selected_sql(model: T, info: Info) -> Optional[Callable[..., Select]]:
    def selected_inner(table_inner: str | None = None):
        return get_only_selected_fields(model, info, table_inner)

    if not info:
        return None
    return selected_inner


class AbstractBL(Generic[T]):
    def __init__(
            self,
            model: type[T],
            info: Info,
            page: int = 1,
            page_size: int = 15
    ):
        self.info = info
        self.sql = get_selected_sql(model, info)
        self.model: T = model
        self.page_size = page_size
        self.offset = (page - 1) * self.page_size

    def _paginate(self, sql: Select, limit: int = None, offset: int = None) -> Select:
        return sql.limit(limit or self.page_size).offset(offset or self.offset)

    def _order(self, sql: Select) -> Select:
        return sql.order_by(desc(self.model.id))

    @staticmethod
    async def _fetch_all(sql: Select, session: AsyncSession = None) -> Sequence[T]:
        return (await session.execute(sql)).scalars().unique().all()

    @staticmethod
    async def _fetch_first(sql: Select, session: AsyncSession = None) -> T:
        return (await session.execute(sql)).scalars().unique().first()

    async def fetch_one(self, obj_id: int, session: AsyncSession = None) -> T:
        return await self._fetch_first(
            self.sql().where(self.model.id == obj_id),
            session
        )

    async def filter_one(self, session: AsyncSession, filters: FilterType = None) -> T | None:
        return await self._fetch_first(
            self.sql().where(*filters),
            session
        )

    async def fetch_all(
            self,
            session: AsyncSession,
            inner: str = None,
            filters: FilterType = None,
            limit: int = None,
            offset: int = None
    ) -> Sequence[T]:
        sql = self.sql(inner)
        if filters:
            sql = sql.where(*filters)
        return await self._fetch_all(
            self._order(self._paginate(sql, limit, offset)),
            session
        )

    async def list_items(
            self,
            session: AsyncSession,
            inner: str = None,
            filters: FilterType = None,
            limit: int = None,
            offset: int = None
    ) -> ListType[T]:
        items = await self.fetch_all(session, inner, filters, limit, offset)
        count = await self.count_items(session, filters)
        return ListType(
            items=items,
            count=count
        )

    async def count_items(self, session: AsyncSession, filters: FilterType = None) -> int:
        sql = select(func.count(self.model.id))
        if filters:
            sql = sql.where(*filters)
        return await self._fetch_first(sql, session)

    async def delete_item(self, obj_id: int, session: AsyncSession = None) -> None:
        await session.execute(
            delete(self.model).where(self.model.id == obj_id)
        )
        await session.commit()

    async def update_item(self, obj_id: int, values: dict, session: AsyncSession = None) -> None:
        await session.execute(
            update(self.model).where(self.model.id == obj_id).values(**values)
        )
        await session.commit()

    async def create_item(self, payload: dict, session: AsyncSession = None) -> T:
        item_id = (await session.execute(
            insert(self.model).values(**payload).returning(self.model.id)
        )).scalars().first()
        await session.commit()
        return self.model(
            id=item_id,
            **payload
        )
