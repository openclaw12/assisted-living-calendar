from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field("sqlite:///./app.db", alias="DATABASE_URL")

    class Config:
        env_file = ("config/dev.env",)
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]
