from sqlalchemy import select

from shared.db import CustomerAddress


def exists_by_id(address_id: int):
    return select(CustomerAddress.id).where(CustomerAddress.id == address_id)
