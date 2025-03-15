from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List,Literal
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="setting.env", env_file_encoding="utf-8")
    kafka_bootstrap_servers: str
    kafka_topic: str
    kraken_pairs: List[str]
    data_source: Literal['live','historical','test'] = Field(alias="DATA_SOURCE")
    last_ndays: int


settings = Settings()
