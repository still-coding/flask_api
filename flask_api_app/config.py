from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="settings.env", extra="ignore")

    mongodb_url: str
    mongodb_dbname: str


settings = Settings()
