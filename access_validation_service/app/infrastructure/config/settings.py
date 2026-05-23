from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Config(BaseSettings):
    DEBUG: bool
    LOG_LEVEL: str

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_CONSUMER_GROUP: str = 'fastapi-app'
    KAFKA_AUTO_OFFSET_RESET: str = 'earliest'  # В проде поставить "latest".

    # Topics
    ACCESSES_TOPIC: str = 'access_requests'

    ACCESS_MANAGEMENT_SERVICE_URL: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_settings() -> Config:
    return Config()  # type: ignore


settings = get_settings()
