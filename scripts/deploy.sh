#!/bin/bash
set -e

cd "$(dirname "$0")/../k8s"

echo "Deploying to Kubernetes..."
kubectl apply -k .

echo "Waiting for MariaDB..."
kubectl -n frappe wait --for=condition=ready pod -l app=mariadb --timeout=120s

echo "Running init job..."
kubectl -n frappe delete job frappe-init --ignore-not-found
kubectl apply -f frappe-init-job.yaml
kubectl -n frappe wait --for=condition=complete job/frappe-init --timeout=300s

echo "Deployment complete!"
kubectl -n frappe get pods
