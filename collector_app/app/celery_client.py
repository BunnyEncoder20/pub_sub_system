import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "collector",
    broker=os.getenv("CELERY_BROKER_URL"),
)

def send_task(data: dict):
    celery_app.send_task("app.tasks.save_to_db", args=[data])
