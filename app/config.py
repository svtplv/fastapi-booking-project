from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    SECRET_KEY: str
    ALGORITHM: str

    @property
    def DATABASE_URL(self):
        return (
            f'postgresql+asyncpg://{self.DB_USER}:'
            f'{self.DB_PASS}@{self.DB_HOST}:'
            f'{self.DB_PORT}/{self.DB_NAME}'
        )

    class Config:
        env_file = '.env'


settings = Settings()
