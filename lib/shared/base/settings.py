from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_PASSWORD: str = 'admin'
    POSTGRES_USER: str = 'admin'
    POSTGRES_DB: str = 'default'
    POSTGRES_HOST: str = 'db'
    POSTGRES_PORT: int = 5432

    SECRET_KEY: str = 'c29tZXNlY3JldGtleWZvcnJlZnJlc2hkcm9wc2hpcDIyODMyMmF6YQ=='
    REFRESH_TOKEN_EXPIRES_IN: int = 43200
    ACCESS_TOKEN_EXPIRES_IN: int = 1440

    @property
    def db_url(self):
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB
        )


settings = Settings()
