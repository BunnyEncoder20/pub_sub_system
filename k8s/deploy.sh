#!/bin/bash

echo "🚀 Deploying pub-sub system to Kubernetes..."

# Apply resources in dependency order
echo "📦 Creating ConfigMap..."
kubectl apply -f configmap.yaml

echo "🐘 Deploying PostgreSQL..."
kubectl apply -f postgres.yaml

echo "🐰 Deploying RabbitMQ..."
kubectl apply -f rabbitmq.yaml

echo "⏳ Waiting for database services to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/postgres
kubectl wait --for=condition=available --timeout=300s deployment/rabbitmq

echo "🔄 Deploying Celery Worker..."
kubectl apply -f celery-worker.yaml

echo "🌐 Deploying FastAPI Collector App..."
kubectl apply -f collector-app.yaml

echo "⏳ Waiting for application services to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/celery-worker
kubectl wait --for=condition=available --timeout=300s deployment/collector-app

echo "✅ Deployment complete!"
echo ""
echo "🔗 To access the FastAPI app from Postman:"
echo "   URL: http://$(minikube ip):30000"
echo ""
echo "🔍 To check the status:"
echo "   kubectl get pods"
echo "   kubectl get services"
echo ""
echo "🐰 To access RabbitMQ management:"
echo "   URL: http://$(minikube ip):$(kubectl get service rabbitmq-management -o jsonpath='{.spec.ports[0].nodePort}')"
echo "   Username: guest"
echo "   Password: guest"
