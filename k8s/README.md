# Kubernetes Deployment for Pub-Sub System

This directory contains Kubernetes manifests to deploy the pub-sub system to a local minikube cluster.

## Prerequisites

1. **minikube** - Local Kubernetes cluster
2. **kubectl** - Kubernetes CLI
3. **Docker images** - Built locally for the applications

## Architecture

The deployment includes:
- **PostgreSQL**: Database with persistent storage
- **RabbitMQ**: Message broker with management interface
- **FastAPI App**: Collector application exposed via NodePort
- **Celery Worker**: Background task processor

## Quick Start

### 1. Build Docker Images for Minikube

First, configure your shell to use minikube's Docker daemon:
```bash
eval $(minikube -p minikube docker-env)
```

Then build your images:
```bash
# Build collector app
docker build -t collector-app:latest ./collector_app

# Build celery worker  
docker build -t celery-worker:latest ./celery_worker
```

### 2. Deploy to Kubernetes

Run the deployment script:
```bash
./k8s/deploy.sh
```

Or deploy manually:
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/rabbitmq.yaml
kubectl apply -f k8s/celery-worker.yaml
kubectl apply -f k8s/collector-app.yaml
```

### 3. Access the Services

#### FastAPI Application
- **URL**: `http://$(minikube ip):30000`
- Use this URL in Postman to test your endpoints

#### RabbitMQ Management Interface
- **URL**: `http://$(minikube ip):<nodeport>`
- **Username**: guest
- **Password**: guest
- Find the NodePort: `kubectl get service rabbitmq-management`

## File Descriptions

- `configmap.yaml`: Environment variables for all services
- `postgres.yaml`: PostgreSQL deployment with persistent storage
- `rabbitmq.yaml`: RabbitMQ deployment with management interface
- `collector-app.yaml`: FastAPI application with external access
- `celery-worker.yaml`: Celery worker deployment
- `deploy.sh`: Automated deployment script
- `cleanup.sh`: Remove all resources

## Useful Commands

```bash
# Check pod status
kubectl get pods

# Check services
kubectl get services

# View logs
kubectl logs -f deployment/collector-app
kubectl logs -f deployment/celery-worker

# Get minikube IP
minikube ip

# Access service URL directly
minikube service collector-app-external --url

# Clean up everything
./k8s/cleanup.sh
```

## Troubleshooting

### Images Not Found
If you see `ImagePullBackOff` errors:
1. Make sure you configured Docker to use minikube's daemon
2. Rebuild the images after configuring the daemon
3. Verify images exist: `docker images | grep -E "(collector-app|celery-worker)"`

### Database Connection Issues
- Check if PostgreSQL pod is running: `kubectl get pods`
- Verify ConfigMap has correct URLs: `kubectl get configmap app-config -o yaml`

### Service Not Accessible
- Get the correct NodePort: `kubectl get services`
- Get minikube IP: `minikube ip`
- Ensure minikube is running: `minikube status`
