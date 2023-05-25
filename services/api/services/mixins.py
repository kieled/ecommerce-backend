from typing import Any, Sequence
from pydantic import BaseModel
from sqlalchemy import desc, delete, insert, update, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.types import Info
from utils import get_only_selected_fields


class ListType(BaseModel):
    items: list[Any] | Sequence[Any]
    count: int


def get_selected_sql(model, info):
    if not info:
        return None

    def selected_inner(table_inner: str | None = None):
        return get_only_selected_fields(model, info, table_inner)

    return selected_inner


class AppService:
    def __init__(
            self,
            db: AsyncSession,
            model,
            info,
            page: int = 1,
            page_size: int = 15
    ):
        self.info: Info = info
        self.sql = get_selected_sql(model, info)
        self.db = db
        self.model = model
        self.page_size = page_size
        self.offset = (page - 1) * self.page_size

    def _paginate(self, sql):
        return sql.limit(self.page_size).offset(self.offset)

    def _order(self, sql):
        return sql.order_by(desc(self.model.id))

    async def _fetch_all(self, sql):
        return (await self.db.execute(sql)).scalars().unique().all()

    async def _fetch_first(self, sql):
        return (await self.db.execute(sql)).scalars().unique().first()

    async def fetch_one(self, obj_id: int):
        return await self._fetch_first(
            self.sql().where(self.model.id == obj_id)
        )

    async def fetch_all(self, inner: str | None = None, filters: list | tuple | None = None):
        sql = self.sql(inner)
        if filters:
            sql = sql.where(*filters)
        return await self._fetch_all(
            self._order(self._paginate(sql))
        )

    async def list_items(self, inner: str | None = None, filters: list | None = None) -> ListType:
        items = await self.fetch_all(inner, filters)
        count = await self.count_items(filters)
        return ListType(
            items=items,
            count=count
        )

    async def count_items(self, filters: list | None = None) -> int:
        sql = select(func.count(self.model.id))
        if filters:
            sql = sql.where(*filters)
        return await self._fetch_first(sql)

    async def delete_item(self, obj_id: int) -> None:
        await self.db.execute(
            delete(self.model).where(self.model.id == obj_id)
        )
        await self.db.commit()

    async def update_item(self, obj_id: int, values: dict):
        await self.db.execute(
            update(self.model).where(self.model.id == obj_id).values(**values)
        )
        await self.db.commit()

    async def create_item(self, payload: dict):
        item_id = (await self.db.execute(
            insert(self.model).values(**payload).returning(self.model.id)
        )).scalars().first()
        await self.db.commit()
        return dict(
            id=item_id,
            **payload
        )
