"""
Shared configuration for the pub-sub system.

This module contains configuration classes for database, RabbitMQ, and other
shared infrastructure components that are used across multiple applications.
"""

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    # PostgreSQL connection settings
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def database_url(self) -> str:
        """Generate the complete database URL."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def async_database_url(self) -> str:
        """Generate the async database URL."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


class RabbitMQSettings(BaseSettings):
    """RabbitMQ configuration settings."""

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_VHOST: str = "/"

    # Queue and Exchange settings
    DEVICE_QUEUE: str = "device_messages"
    EXCHANGE_NAME: str = "device_exchange"
    ROUTING_KEY: str = "device.message"

    @property
    def connection_url(self) -> str:
        """Generate the complete RabbitMQ connection URL."""
        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}{self.RABBITMQ_VHOST}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


class AppSettings(BaseSettings):
    """General application settings."""

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    # API settings
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"
        extra = "ignore"


# Global instances of settings
database_settings = DatabaseSettings()
rabbitmq_settings = RabbitMQSettings()
app_settings = AppSettings()


class SharedSettings:
    """Combined settings for shared infrastructure."""
    
    def __init__(self):
        self.database = database_settings
        self.rabbitmq = rabbitmq_settings
        self.app = app_settings


# Global instance of shared settings
shared_settings = SharedSettings()
