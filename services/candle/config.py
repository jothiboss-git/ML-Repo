from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="setting.env", env_file_encoding="utf-8")
    kafka_bootstrap_servers: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str
    candle_seconds: int
    emit_incomplete_candle : bool
    data_source: Literal['live','historical','test']

settings = Settings()
