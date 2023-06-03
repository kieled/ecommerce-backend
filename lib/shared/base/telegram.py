from pydantic import BaseSettings


class TelegramSettings(BaseSettings):
    TG_BOT_TOKEN: str = ''
    TG_APP_ID: int = 0
    TG_APP_HASH: str = ''


telegram_config = TelegramSettings()
