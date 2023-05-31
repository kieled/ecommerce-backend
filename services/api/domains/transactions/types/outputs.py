import strawberry


@strawberry.type(name='PublicOrderRequisite')
class TransactionRequisiteType:
    id: int = 0
    info: str = ''
    detail: str | None = None


@strawberry.type(name='Promo')
class PromoType:
    id: int = 0
    discount: float = 0


@strawberry.type(name='PublicOrderDetail')
class TransactionDetailPublicType:
    amount: str = ''
    currency: int = 3
    requisite: TransactionRequisiteType = strawberry.field(default_factory=TransactionRequisiteType)
    promo: PromoType | None = None


__all__ = [
    'PromoType',
    'TransactionDetailPublicType',
    'TransactionRequisiteType',
]
