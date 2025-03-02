from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="setting.env", env_file_encoding="utf-8")
    kafka_bootstrap_servers: str
    kafka_topic: str
    kraken_pairs: List[str]


settings = Settings()
