from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field("postgresql+psycopg://alc:alc@localhost:5432/alc_dev", alias="DATABASE_URL")

    class Config:
        env_file = ("config/dev.env",)
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]
