import strawberry

from ..enums import transaction_currency_enum


@strawberry.type(name='RequisitesItem')
class RequisitesItemType:
    id: int
    type_id: int = 0
    info: str = ''
    is_active: bool = False
    detail: str = ''


@strawberry.type(name='RequisitesTypeItem')
class RequisitesTypeItemType:
    id: int
    name: str = ''
    detail: str = ''
    currency: transaction_currency_enum = transaction_currency_enum.byn
