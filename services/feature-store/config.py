from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List
from typing import Literal 
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="setting.env", env_file_encoding="utf-8")
    kafka_bootstrap_servers: str
    kafka_input_topic: str
    kafka_consumer_group: str
    feature_group_name: str
    feature_group_version: int
    feature_group_primary_key: List[str]
    feature_group_event_time: str   
    feature_group_mateization_interval: Optional[int] = 15
    data_source: Literal['live','historical','test']

class HopsworksConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file="credentials.env", env_file_encoding="utf-8")
    hopsworks_api_key: str
    hopsworks_project_name: str

settings = Settings()
hopsworks_config = HopsworksConfig()
