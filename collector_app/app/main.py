from fastapi import FastAPI
from app.celery_client import send_task

app = FastAPI()

@app.post("/publish")
def publish(data: dict):
    send_task(data)
    return {"status": "task sent"}
