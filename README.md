# Pub-Sub System

## About the Project

## Tech Stack
1. API: FastAPI
1. Task Queue: Celery
1. Broker: RabbitMQ
1. DB: PostgreSQL
1. Worker: Celery Worker
1. Optional Monitoring: Flower (Web UI for Celery tasks)


## Project Planning

### Project Architecture
```bash
+------------------+
|  collector_app   |   <-- FastAPI + Celery producer
+--------+---------+
         |
         | .delay() (Celery task)
         v
+--------+---------+
|    RabbitMQ      |
+--------+---------+
         |
         v
+--------+---------+
|  celery_worker   |   <-- Executes task
|  (writes to DB)  |
+--------+---------+
         |
         v
    PostgreSQL
```

### Project Structure
```bash
microservice-system/
│
├── docker-compose.yml
│
├── collector_app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   └── app/
│       ├── main.py
│       └── celery_client.py
│
├── celery_worker/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   └── app/
│       ├── tasks.py
│       ├── db.py
│       └── models.py
```

## Important Commands
- to build micro services containers:
```bash
docker-compose up --build
```
