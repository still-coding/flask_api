from typing import Union

from pydantic import AnyUrl, FilePath, NewPath, PositiveInt

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env_settings", extra="ignore")

    mongodb_url: AnyUrl
    mongodb_dbname: str


settings = Settings()
