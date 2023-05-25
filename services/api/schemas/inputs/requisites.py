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


@strawberry.input
class RequisiteTypeCreateInput:
    name: str
    detail: str


@strawberry.input
class RequisiteTypeItemInput:
    id: int
    name: str | None = None
    detail: str | None = None
