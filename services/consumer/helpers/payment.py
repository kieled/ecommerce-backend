import logging

import aiohttp
from sqlalchemy import update

from shared.db import Transaction, TransactionStatusEnum, scoped_session


async def send_payment_request(
        transaction_id: int,
        amount: int,
        payment_type: str,
        latest_ids: list[str]
):
    bank_id: str | None = None

    async with aiohttp.ClientSession() as s:
        try:
            async with s.post('http://payment:8000/check', data={
                'amount': amount,
                'payment_type': payment_type,
                'latest_ids': latest_ids
            }) as response:
                data = await response.json()
                bank_id = data.get('transaction_id')
        except Exception as e:
            logging.error(e)

    if bank_id:
        values = dict(
            status=TransactionStatusEnum.complete,
            bank_number_id=bank_id
        )
    else:
        values = dict(
            status=TransactionStatusEnum.canceled,
            promo_id=None
        )

    async with scoped_session() as s:
        await s.execute(
            update(Transaction).values(**values).where(Transaction.id == transaction_id)
        )
        await s.commit()
    return bank_id
