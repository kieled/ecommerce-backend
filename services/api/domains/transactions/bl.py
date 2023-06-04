import math
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from shared.db import Transaction, TransactionStatusEnum, cls_session, Promo
from .types import transaction_status_enum
from . import sql
from api.utils.graphql import get_user_ids
from api.domains.mixin import AbstractBL


@cls_session
class TransactionBL(AbstractBL[Transaction]):

    def _filters(self, transaction_id: int) -> tuple:
        temp_user_id, user_id = get_user_ids(self.info)

        return (
            Transaction.id == transaction_id,
            Transaction.temp_user_id == temp_user_id
            if temp_user_id
            else Transaction.user_id == user_id
        )

    async def get(self, transaction_id: int, session: AsyncSession = None) -> Transaction | None:
        return await self.filter_one(session, self._filters(transaction_id))

    async def detail(self, transaction_id: int, session: AsyncSession = None) -> Transaction | None:
        return await self.fetch_one(transaction_id, session)

    async def list(self, status: transaction_status_enum, session: AsyncSession = None):
        filters = (Transaction.status == TransactionStatusEnum(status.value),) if status else None
        return await self.list_items(session, 'items', filters)

    async def confirm(self, transaction_id: int, session=None) -> dict:
        # TODO: add filtering transaction through user_ids
        current_transaction: Transaction = (await session.execute(
            sql.get_current(transaction_id)
        )).scalars().first()

        if not current_transaction:
            raise Exception('Transaction not found')

        from_date = datetime.now() - timedelta(hours=2)

        latest_ids = (await session.execute(
            sql.latest_ids(from_date)
        )).scalars().all()

        await session.execute(
            sql.mark_success(self._filters(transaction_id))
        )
        await session.commit()

        return dict(
            transaction_id=transaction_id,
            amount=current_transaction.amount,
            payment_type=current_transaction.requisite.type.name,
            latest_ids=[str(i) for i in latest_ids]
        )

    async def public_list(self, session: AsyncSession = None):
        temp_user_id, user_id = get_user_ids(self.info)
        filters = (
            Transaction.temp_user_id == temp_user_id if temp_user_id else Transaction.user_id == user_id,
        )
        return await self.list_items(session, filters=filters)

    async def create(
            self,
            amount: int,
            requisite_id: int,
            promo: Promo | None,
            session: AsyncSession = None
    ) -> int:
        temp_user_id, user_id = get_user_ids(self.info)

        if promo:
            amount = math.ceil(amount - amount * promo.discount)

        transaction = await self.create_item(dict(
            amount=amount,
            promo_id=promo,
            user_id=user_id,
            temp_user_id=temp_user_id,
            requisite_id=requisite_id
        ), session)

        if not transaction:
            raise Exception("Transaction couldn't be created")

        return transaction.id
