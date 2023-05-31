from sqlalchemy import select, update
from sqlalchemy.orm import load_only

from shared.db import Requisites


def active_id(type_id: int):
    return select(Requisites).options(load_only(Requisites.id)).where(
        Requisites.is_active == True,
        Requisites.type_id == type_id
    )


def deactivate(item_id: int):
    return update(Requisites).where(
        Requisites.id == item_id
    ).values(
        is_active=False
    )
