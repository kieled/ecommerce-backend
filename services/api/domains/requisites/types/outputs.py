import strawberry


@strawberry.type(name='RequisitesItem')
class RequisitesItemType:
    id: int
    type_id: int = 0
    info: str = ''
    is_active: bool = False
    detail: str = ''


__all__ = [
    'RequisitesItemType',
]
