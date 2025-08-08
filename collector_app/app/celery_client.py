from celery import Celery
from app.config import settings

celery_app = Celery(
    "collector",
    broker=settings.CELERY_BROKER_URL,
)

def send_task(task_name, payload):
    celery_app.send_task(task_name, args=[payload])
