from typing import Literal
from pydantic import BaseModel


class YandexItemSchema(BaseModel):
    operation_id: str
    amount: float
    direction: Literal['out', 'in']
    status: Literal['success', 'refused', 'in_progress']
