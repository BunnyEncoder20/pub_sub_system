from fastapi import FastAPI, Depends
from app.celery_client import send_task
from app.db import get_db_session
from app.models import DataItem
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.config import settings
from app.routers import device, location

app = FastAPI()

app.include_router(device.router)
app.include_router(location.router)

class PublishData(BaseModel):
    content: str

@app.post("/publish")
def publish(data: PublishData, session: Session = Depends(get_db_session)):
    send_task(data.dict())
    return {"status": "task sent"}

@app.get("/data")
def get_data(session: Session = Depends(get_db_session)):
    items = session.query(DataItem).all()
    return items
