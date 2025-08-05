from celery import Celery
from app.config import settings

celery_app = Celery(
    "collector",
    broker=settings.CELERY_BROKER_URL,
)

def send_task(data: dict):
    celery_app.send_task("app.tasks.save_to_db", args=[data])
