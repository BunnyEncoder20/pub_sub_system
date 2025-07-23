"""
Consumer app specific configuration.

This module contains configuration settings specific to the consumer application,
such as consumer-specific settings, processing options, and feature flags.
"""

from pydantic_settings import BaseSettings
from shared.config import shared_settings


class ConsumerAppSettings(BaseSettings):
    """Consumer application specific settings."""

    # Consumer settings
    APP_NAME: str = "Message Consumer"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Consumes messages from queue and processes them"

    # Processing settings
    WORKER_COUNT: int = 1
    PREFETCH_COUNT: int = 10
    MAX_RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 5  # seconds

    # Consumer specific settings
    CONSUMER_TAG: str = "device_consumer"
    AUTO_ACK: bool = False
    HEARTBEAT_INTERVAL: int = 30  # seconds

    # Processing options
    PROCESS_BATCH_SIZE: int = 50
    PROCESS_TIMEOUT: int = 30  # seconds

    # Feature flags
    ENABLE_DEAD_LETTER_QUEUE: bool = True
    ENABLE_MESSAGE_PERSISTENCE: bool = True
    ENABLE_MONITORING: bool = True

    class Config:
        env_file = ".env"
        env_prefix = "CONSUMER_"


# Consumer app settings instance
consumer_settings = ConsumerAppSettings()

# For easy access to shared settings
settings = shared_settings
