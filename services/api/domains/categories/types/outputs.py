import strawberry


@strawberry.type(name='ProductCategory')
class ProductCategoryType:
    id: int = 0
    slug: str = ''
    name: str = ''


@strawberry.type(name='PublicCategory')
class PublicCategoryType:
    id: int = 0
    name: str = ''


__all__ = [
    'ProductCategoryType',
    'PublicCategoryType'
]
