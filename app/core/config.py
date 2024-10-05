import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from consts import LOG_DEFAULT_FORMAT


class ApiPrefix(BaseModel):
    prefix: str = "/api/v1"


class DatabaseConfig(BaseModel):
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class DatabaseCreds(BaseModel):
    user: str
    password: str
    name: str
    port: int
    service: str


class RedisConfig(BaseModel):
    service: str
    port: int


class AppConfig(BaseModel):
    mode: Literal["DEV", "TEST", "PROD"]


class LoggingConfig(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    format: str = LOG_DEFAULT_FORMAT
    status: int = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.DEBUG,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }


class Settings(BaseSettings):
    app: AppConfig
    logging: LoggingConfig
    db: DatabaseCreds
    test: DatabaseCreds
    redis: RedisConfig
    api: ApiPrefix = ApiPrefix()
    db_config: DatabaseConfig = DatabaseConfig()
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="_",
        env_file=(Path(__file__).parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.db.user}:{self.db.password}@{self.db.service}:{self.db.port}/{self.db.name}"

    @property
    def test_database_url(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.test.user}:{self.test.password}@{self.test.service}:{self.test.port}/{self.test.name}"


settings = Settings()
print(settings)
