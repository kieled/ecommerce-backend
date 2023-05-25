from pydantic import BaseSettings


class TelegramSettings(BaseSettings):
    TG_BOT_TOKEN: str
    TG_APP_ID: int
    TG_APP_HASH: str


telegram_config = TelegramSettings()
