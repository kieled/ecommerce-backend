import strawberry


@strawberry.input
class TelegramUserInput:
    auth_date: str
    first_name: str | None = None
    last_name: str | None = None
    photo_url: str | None = None
    hash: str
    id: str
    username: str | None = None
