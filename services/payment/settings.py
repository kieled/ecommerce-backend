from pydantic import BaseSettings


class Settings(BaseSettings):
    YANDEX_TOKEN: str


settings = Settings()

__all__ = [
    'settings'
]
