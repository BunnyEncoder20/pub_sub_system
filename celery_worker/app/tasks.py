from celery import Celery
from app.db import get_db_session
from app.models import DataItem
from app.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
)

@celery_app.task(name="app.tasks.save_to_db")
def save_to_db(data: dict):
    session = get_db_session()
    item = DataItem(content=data.get("content"))
    session.add(item)
    session.commit()
    session.close()
    print("Saved to DB:", data)
