from celery import Celery
import os

from app.db import get_db_session
from app.models import DataItem
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL"),
)

@celery_app.task(name="app.tasks.save_to_db")
def save_to_db(data: dict):
    session = get_db_session()
    item = DataItem(content=str(data))
    session.add(item)
    session.commit()
    session.close()
    print("Saved to DB:", data)
