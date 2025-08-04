# Pub-Sub System

## About the Project
This project is a simple microservices-based pub-sub system. It consists of two main services:

- **`collector_app`**: A FastAPI web application that acts as the producer. It exposes a `/publish` endpoint to receive data.
- **`celery_worker`**: A Celery worker that acts as the consumer. It listens for tasks from the message broker and saves the data to a PostgreSQL database.

The services communicate with each other using RabbitMQ as a message broker.

## Tech Stack
- API: FastAPI
- Task Queue: Celery
- Broker: RabbitMQ
- DB: PostgreSQL
- Worker: Celery Worker
- Optional Monitoring: Flower (Web UI for Celery tasks)

## Project Architecture
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

## Project Structure
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

## How to Use

1. **Start the services:**
   ```bash
   docker-compose up --build
   ```

2. **Send data to the collector:**
   Use a tool like `curl` to send a POST request to the `/publish` endpoint:
   ```bash
   curl -X POST "http://localhost:8000/publish" -H "Content-Type: application/json" -d '{"key": "value"}'
   ```

3. **Verify the data:**
   You can check the logs of the `celery_worker` to see the data being processed and saved.
   ```bash
   docker-compose logs -f celery_worker
   ```
   You should see a log message like `Saved to DB: {'key': 'value'}`.

## Important Commands
- **Build and run the services in the background:**
  ```bash
  docker-compose up --build -d
  ```
- **Run the services in the background:**
  ```bash
  docker-compose up -d
  ```
- **Stop the services:**
  ```bash
  docker-compose down
  ```
- **View logs:**
  ```bash
  docker-compose logs -f <service_name>
  ```
  (e.g., `collector_app`, `celery_worker`)