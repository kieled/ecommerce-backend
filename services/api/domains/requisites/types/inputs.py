import strawberry


@strawberry.input
class RequisitesItemInput:
    id: int
    type_id: int
    info: str | None = None
    is_active: bool | None = None
    detail: str | None = None


@strawberry.input
class RequisitesCreateInput:
    type_id: int
    info: str
    detail: str


__all__ = [
    'RequisitesCreateInput',
    'RequisitesItemInput',
]
