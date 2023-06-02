from sqlalchemy import select

from shared.db import Promo


def find(promo: str):
    return select(Promo).where(
        Promo.code == promo,
        ~Promo.transaction.has()
    )
