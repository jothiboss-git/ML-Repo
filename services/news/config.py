from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class CryptopanicConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="cryptopanic_credential.env",
        env_file_encoding="utf-8"
       
       
    )
    cryptopanic_api_key: str

cryptopanic_config = CryptopanicConfig()

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="setting.env",
        env_file_encoding="utf-8"
        
    )
    kafka_bootstrap_servers: str
    kafka_topic: str
    polling_interval: int = 10  # seconds

settings = Config()