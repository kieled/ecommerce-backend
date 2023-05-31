import strawberry

from shared.db import TransactionStatusEnum

transaction_status_enum = strawberry.enum(TransactionStatusEnum)

__all__ = [
    'transaction_status_enum',
]
