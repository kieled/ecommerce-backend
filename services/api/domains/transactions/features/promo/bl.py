from sqlalchemy.ext.asyncio import AsyncSession

from api.domains.mixin import AbstractBL
from shared.db import Promo, cls_session
from . import sql


@cls_session
class PromoBL(AbstractBL[Promo]):
    @staticmethod
    async def find(promo: str, session: AsyncSession = None) -> Promo | None:
        return (await session.execute(sql.find(promo))).scalars().first()
