import enum


class ImageCropDirectionEnum(enum.Enum):
    top = 'top'
    bottom = 'bottom'


class ProductStatusEnum(enum.IntEnum):
    created = 1
    published = 2
    archive = 3


class CurrencyEnum(enum.Enum):
    usd = 'usd'
    rub = 'rub'


class TransactionStatusEnum(enum.Enum):
    created = 'created'
    confirmed = 'confirmed'
    complete = 'complete'
    canceled = 'canceled'


class TransactionCurrencyEnum(enum.IntEnum):
    byn = 1
    rub = 2
    usd = 3


class UserTypeEnum(enum.IntEnum):
    user = 1
    admin = 2
