#!/bin/bash

echo "🧹 Cleaning up pub-sub system from Kubernetes..."

echo "🗑️  Removing application deployments..."
kubectl delete -f collector-app.yaml --ignore-not-found=true
kubectl delete -f celery-worker.yaml --ignore-not-found=true

echo "🗑️  Removing database services..."
kubectl delete -f rabbitmq.yaml --ignore-not-found=true
kubectl delete -f postgres.yaml --ignore-not-found=true

echo "🗑️  Removing ConfigMap..."
kubectl delete -f configmap.yaml --ignore-not-found=true

echo "✅ Cleanup complete!"

echo ""
echo "🔍 Remaining resources:"
kubectl get pods,services,pvc
