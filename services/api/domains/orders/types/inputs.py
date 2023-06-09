import strawberry


@strawberry.input
class UpdateOrderInput:
    order_id: int
    order_url: str | None = None
    track_code: str | None = None


__all__ = [
    'UpdateOrderInput',
]
