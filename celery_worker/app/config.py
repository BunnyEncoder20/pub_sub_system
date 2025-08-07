from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_URL: str
    CELERY_BROKER_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
