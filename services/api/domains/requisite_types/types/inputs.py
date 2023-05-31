import strawberry


@strawberry.input
class RequisiteTypeCreateInput:
    name: str
    detail: str


@strawberry.input
class RequisiteTypeItemInput:
    id: int
    name: str | None = None
    detail: str | None = None


__all__ = [
    'RequisiteTypeItemInput',
    'RequisiteTypeCreateInput',
]
