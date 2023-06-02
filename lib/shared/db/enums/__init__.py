from enum import Enum, auto, IntEnum


class ImageCropDirectionEnum(Enum):
    top = auto()
    bottom = auto()


class ProductStatusEnum(IntEnum):
    created = 1
    published = 2
    archive = 3


class CurrencyEnum(Enum):
    usd = auto()
    rub = auto()


class TransactionStatusEnum(Enum):
    created = auto()
    confirmed = auto()
    complete = auto()
    canceled = auto()


class UserTypeEnum(IntEnum):
    user = 1
    admin = 2
