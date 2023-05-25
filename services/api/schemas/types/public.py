import strawberry


@strawberry.type(name='PublicParamItem')
class PublicParamItemType:
    id: int
    name: str = ''
    value: str = ''


@strawberry.type(name='PublicImage')
class PublicImageType:
    id: int
    path: str = ''


@strawberry.type(name='PublicSize')
class PublicSizeType:
    id: int
    size: str = ''
    name: str | None = None


@strawberry.type(name='PublicStockItem')
class PublicStockItemType:
    id: int
    image: str = ''
    color: str = ''
    name: str | None = None
    sizes: list[PublicSizeType] = strawberry.field(default_factory=list)


@strawberry.type(name='PublicItem')
class PublicItemType:
    id: int
    title: str = ''
    price: str = ''
    images: list[PublicImageType] = strawberry.field(default_factory=list)


@strawberry.type(name='PublicCategory')
class PublicCategoryType:
    id: int = 0
    name: str = ''


@strawberry.type(name='PublicDetail')
class PublicDetailType:
    id: int
    title: str = ''
    price: str = ''
    description: str = ''

    category: PublicCategoryType = strawberry.field(default=PublicCategoryType)
    images: list[PublicImageType] = strawberry.field(default_factory=list)
    stocks: list[PublicStockItemType] = strawberry.field(default_factory=list)
    params: list[PublicParamItemType] = strawberry.field(default_factory=list)


@strawberry.type(name='PublicList')
class PublicListType:
    products: list[PublicItemType] = strawberry.field(default_factory=list)
    count: int = ''
