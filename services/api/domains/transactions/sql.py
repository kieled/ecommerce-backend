from datetime import datetime
from typing import Iterable

from sqlalchemy import select, update
from sqlalchemy.orm import load_only, joinedload

from shared.db import Transaction, Requisites, RequisiteTypes, TransactionStatusEnum


def get_current(transaction_id: int):
    return select(Transaction).options(
        load_only(Transaction.amount),
        joinedload(
            Transaction.requisite
        ).load_only(Requisites.id).joinedload(
            Requisites.type
        ).load_only(RequisiteTypes.detail)
    ).where(
        Transaction.id == transaction_id
    )


def latest_ids(from_date: datetime):
    return select(Transaction.bank_number_id).where(
        Transaction.bank_number_id != None,
        Transaction.status == TransactionStatusEnum.complete,
        Transaction.updated_at > from_date
    )


def mark_success(filters: Iterable):
    update(Transaction).where(
        *filters,
        Transaction.status == TransactionStatusEnum.created
    ).values(
        status=TransactionStatusEnum.confirmed
    )
