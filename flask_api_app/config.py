from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="settings.env", extra="ignore")

    mongodb_url: str
    mongodb_dbname: str
    redis_host: str
    redis_port: int


settings = Settings()
