import strawberry
from alchemy_graph import orm_to_strawberry
from sqlalchemy import select
from shared.db import Promo, scoped_session
from ..types import TransactionDetailPublicType
from ..bl import TransactionBL
from api.domains.orders.types import OrderPublicListType, OrderPublicTransactionType, PromoResponseType
from api.utils.graphql import IsAuthenticated


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
        data = await TransactionBL(info, page).public_list()
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
        data = await TransactionBL(info).get(order_id)
        return orm_to_strawberry(data, TransactionDetailPublicType)

    @strawberry.field(
        description='Check promo code'
    )
    async def check_promo(
            self, promo_code: str
    ) -> PromoResponseType:
        async with scoped_session() as s:
            result = (await s.execute(
                select(Promo).where(
                    Promo.code == promo_code,
                    ~Promo.transaction.has()
                )
            )).scalars().first()
        if result:
            return PromoResponseType(status=True, discount=result.discount)
        return PromoResponseType(status=False)
