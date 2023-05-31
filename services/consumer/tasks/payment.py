from .telegram import admin_message
from consumer.helpers import send_payment_request


async def check(
        transaction_id: int,
        amount: int,
        payment_type: str,
        latest_ids: list[str]
):
    bank_id = await send_payment_request(transaction_id, amount, payment_type, latest_ids)
    if bank_id:
        await admin_message()
        return dict(
            bank_transaction_id=bank_id
        )


__all__ = ['check']
