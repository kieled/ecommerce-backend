import logging

from sqlalchemy import update

from shared.db import Transaction, TransactionStatusEnum, scoped_session
from .telegram import admin_message


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


async def check(
        transaction_id: int,
        amount: int,
        payment_type: str,
        latest_ids: list[str]
):
    bank_id = await send_payment_request(transaction_id, amount, payment_type, latest_ids)
    if bank_id:
        await admin_message()
        admin_chat_id = loop.run_until_complete(get_current_admin_chat())
        if admin_chat_id:
            loop.run_until_complete(send_telegram_admin_message(admin_chat_id))
        return dict(
            bank_transaction_id=bank_id
        )


__all__ = ['check']
