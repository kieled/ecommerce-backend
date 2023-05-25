from datetime import datetime, timedelta
from sqlalchemy import update, select, func
from sqlalchemy.orm import load_only, joinedload
from shared.db import Transaction, TransactionStatusEnum, Requisites, RequisiteTypes
from api.schemas import transaction_status_enum
from api.utils import get_user_ids
from .mixins import AppService


class TransactionService(AppService):
    def __init__(self, db, info, *args):
        super().__init__(db, Transaction, info, *args)

    def _filters(self, transaction_id: int) -> tuple:
        temp_user_id, user_id = get_user_ids(self.info)

        return (
            Transaction.id == transaction_id,
            Transaction.temp_user_id == temp_user_id
            if temp_user_id
            else Transaction.user_id == user_id
        )

    async def get(self, transaction_id: int) -> Transaction:
        transaction = await self._fetch_first(
            self.sql().where(*self._filters(transaction_id))
        )
        if not transaction:
            raise Exception("Not found")
        return transaction

    async def detail(self, transaction_id: int) -> Transaction:
        transaction = await self.fetch_one(transaction_id)
        if not transaction:
            raise Exception('Not found')
        return transaction

    async def list(self, status: transaction_status_enum):
        return await self.list_items(
            'items',
            [Transaction.status == TransactionStatusEnum(status.value)] if status else None
        )

    async def confirm_public_payment(self, transaction_id: int) -> list:
        sql = select(Transaction).options(
            load_only(Transaction.amount),
            joinedload(
                Transaction.requisite
            ).load_only(Requisites.id).joinedload(
                Requisites.type
            ).load_only(RequisiteTypes.detail)
        ).where(
            Transaction.id == transaction_id
        )
        current_transaction = (await self.db.execute(sql)).scalars().first()

        if not current_transaction:
            raise Exception('Order not found')

        from_data = datetime.now() - timedelta(hours=2)

        sql = select(Transaction.bank_number_id).where(
            Transaction.bank_number_id != None,
            Transaction.status == TransactionStatusEnum.complete,
            Transaction.updated_at > from_data
        )
        latest_ids = (await self.db.execute(sql)).scalars().all()

        sql = update(Transaction).where(
            *self._filters(transaction_id),
            Transaction.status == TransactionStatusEnum.created
        ).values(
            status=TransactionStatusEnum.confirmed
        )

        await self.db.execute(sql)
        await self.db.commit()

        payment_type = 'bnb' if current_transaction.requisite.type.detail == 'ЕРИП' else 'ya'

        return [transaction_id, current_transaction.amount, payment_type, [str(i) for i in latest_ids]]

    async def public_list(self):
        temp_user_id, user_id = get_user_ids(self.info)
        filters = (
            Transaction.temp_user_id == temp_user_id if temp_user_id else Transaction.user_id == user_id,
        )
        items = await self.fetch_all('items', filters)
        count = await self._fetch_first(
            select(func.count(Transaction.id)).where(*filters)
        )
        return dict(
            items=items,
            count=count
        )
