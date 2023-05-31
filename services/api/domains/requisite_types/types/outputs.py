import strawberry


@strawberry.type(name='RequisitesTypeItem')
class RequisitesTypeItemType:
    id: int
    name: str = ''
    detail: str = ''


__all__ = [
    'RequisitesTypeItemType',
]
