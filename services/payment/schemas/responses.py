from pydantic import BaseModel


class PaymentResponse(BaseModel):
    transaction_id: str
