# Pub-Sub Microservice System

A microservice system consisting of two FastAPI applications connected via RabbitMQ:
- **Collector App**: Handles device-related operations and publishes messages
- **Consumer App**: Consumes messages from RabbitMQ and saves to PostgreSQL

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Collector     │───▶│    RabbitMQ     │───▶│    Consumer     │───▶│   PostgreSQL    │
│     App         │    │                 │    │      App        │    │                 │
│   (FastAPI)     │    │                 │    │   (FastAPI)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Project Structure
```zsh
pub-sub-system/
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── Makefile
├── scripts/
│   ├── setup.sh
│   ├── start-dev.sh
│   └── test.sh
├── shared/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── device.py
│   │   └── message.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── device.py
│   ├── rabbitmq/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── publisher.py
│   └── database/
│       ├── __init__.py
│       ├── connection.py
│       └── base.py
├── collector_app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   └── devices.py
│   │   │   └── api.py
│   │   └── deps.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── device_service.py
│   ├── Dockerfile
│   └── requirements.txt
├── consumer_app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── consumer_service.py
│   │   └── database_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── device_repository.py
│   ├── Dockerfile
│   └── requirements.txt
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── collector_app/
│   │   ├── __init__.py
│   │   └── test_devices.py
│   ├── consumer_app/
│   │   ├── __init__.py
│   │   └── test_consumer.py
│   └── shared/
│       ├── __init__.py
│       └── test_rabbitmq.py
├── migrations/
│   ├── __init__.py
│   └── versions/
└── monitoring/
    ├── prometheus/
    │   └── prometheus.yml
    └── grafana/
        └── dashboards/
```

## Quick Start

1. Copy environment file:
```bash
cp .env.example .env
```

2. Start all services:
```bash
docker-compose up -d
```

3. Check service health:
- Collector App: http://localhost:8001/health
- Consumer App: http://localhost:8002/health
- RabbitMQ Management: http://localhost:15672 (guest/guest)

## Services

### Collector App (Port 8001)
- Device CRUD operations
- Message publishing to RabbitMQ
- Health checks

### Consumer App (Port 8002)
- Message consumption from RabbitMQ
- Database operations
- Health checks

## Development

### Prerequisites
- Docker & Docker Compose
- Python 3.9+

### Environment Variables
See `.env.example` for required environment variables.

### Useful Commands
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f collector_app
docker-compose logs -f consumer_app

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

#------------------------------------------------
# RabbitMQ (standalone) docker Image
docker run -d --name rabbitmq-mgmt -p 5672:5672 -p 15672:15672 rabbitmq:3-management-alpine

# Stop the container
docker stop rabbitmq-mgmt

# Start the container again
docker start rabbitmq-mgmt

# View logs
docker logs rabbitmq-mgmt

# Remove the container (when you're done)
docker rm -f rabbitmq-mgmt
```

---

## RabbitMQ
- Run the docker image for Rabbitmq (use cmd given above)
- Management portal at: `http://localhost:15672`
