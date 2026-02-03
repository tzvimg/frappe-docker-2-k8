#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
K8S_DIR="$SCRIPT_DIR/../k8s"

# Use Tanzu kustomization
cd "$K8S_DIR"
cp kustomization-tanzu.yaml kustomization.yaml

echo "=== Deploying Frappe to Tanzu Kubernetes ==="

# Apply all resources
kubectl apply -k .

echo "Waiting for MariaDB to be ready..."
kubectl -n frappe wait --for=condition=ready pod -l app=mariadb --timeout=180s

echo "Waiting for Redis..."
kubectl -n frappe wait --for=condition=ready pod -l app=redis-cache --timeout=60s
kubectl -n frappe wait --for=condition=ready pod -l app=redis-queue --timeout=60s

echo "Waiting for Frappe pod (includes init)..."
kubectl -n frappe wait --for=condition=ready pod -l app=frappe --timeout=600s

echo ""
echo "=== Deployment Complete ==="
kubectl -n frappe get pods
echo ""
echo "Get ingress IP:"
echo "  kubectl -n frappe get ingress"
