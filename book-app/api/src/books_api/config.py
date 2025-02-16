from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    pg_dsn: PostgresDsn


config = Config()
