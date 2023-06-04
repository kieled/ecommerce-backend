from dataclasses import dataclass
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared.db import CustomerAddress, Transaction


@dataclass
class MigrationService:
    db: AsyncSession

    async def from_temp(self, temp_user_id: str, user_id: int):
        addresses_sql = select(CustomerAddress.id).where(
            CustomerAddress.temp_user_id == temp_user_id
        )
        addresses_ids = (await self.db.execute(addresses_sql)).scalars().all()

        if len(addresses_ids):
            addresses_sql = update(CustomerAddress).where(
                CustomerAddress.id.in_(addresses_ids)
            ).values(
                temp_user_id=None,
                user_id=user_id
            )
            await self.db.execute(addresses_sql)
            transactions_sql = update(Transaction).values(
                temp_user_id=None,
                user_id=user_id
            ).where(
                Transaction.temp_user_id == temp_user_id
            )
            await self.db.execute(transactions_sql)
            await self.db.commit()
