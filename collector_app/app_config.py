"""
Collector app specific configuration.

This module contains configuration settings specific to the collector application,
such as FastAPI settings, collector-specific ports, and feature flags.
"""

from pydantic_settings import BaseSettings
from shared.config import shared_settings


class CollectorAppSettings(BaseSettings):
    """Collector application specific settings."""
    
    # FastAPI settings
    APP_NAME: str = "Device Data Collector"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Collects device data and publishes to message queue"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    
    # Collector specific settings
    MAX_MESSAGE_SIZE: int = 1024 * 1024  # 1MB
    BATCH_SIZE: int = 100
    BATCH_TIMEOUT: int = 5  # seconds
    
    # Feature flags
    ENABLE_BATCH_PROCESSING: bool = True
    ENABLE_MESSAGE_VALIDATION: bool = True
    ENABLE_METRICS: bool = True
    
    class Config:
        env_file = ".env"
        env_prefix = "COLLECTOR_"


# Collector app settings instance
collector_settings = CollectorAppSettings()

# For backward compatibility and easy access to shared settings
settings = shared_settings
