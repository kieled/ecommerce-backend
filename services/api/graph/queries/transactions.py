import strawberry
from sqlalchemy import select
from config import session
from models import Promo
from schemas import OrderPublicListType, TransactionDetailPublicType, \
    PromoResponseType, OrderPublicTransactionType
from services import TransactionService
from utils import orm_to_strawberry, IsAuthenticated


@strawberry.type
class TransactionQuery:
    @strawberry.field(
        description='Order public list',
        permission_classes=[IsAuthenticated]
    )
    async def order_public_list(
            self,
            info,
            page: int | None = 1
    ) -> OrderPublicListType:
        async with session() as s:
            data = await TransactionService(s, info, page).public_list()
        return OrderPublicListType(
            items=[orm_to_strawberry(i, OrderPublicTransactionType) for i in data['items']],
            count=data['count']
        )

    @strawberry.field(
        description='Order public detail',
        permission_classes=[IsAuthenticated]
    )
    async def order_public_detail(
            self, order_id: int, info
    ) -> TransactionDetailPublicType:
        async with session() as s:
            data = await TransactionService(s, info).get(order_id)
        data = orm_to_strawberry(data, TransactionDetailPublicType)
        return data

    @strawberry.field(
        description='Check promo code'
    )
    async def check_promo(
            self, promo_code: str
    ) -> PromoResponseType:
        async with session() as s:
            result = (await s.execute(
                select(Promo).where(
                    Promo.code == promo_code,
                    ~Promo.transaction.has()
                )
            )).scalars().first()
        if result:
            return PromoResponseType(status=True, discount=result.discount)
        return PromoResponseType(status=False)
