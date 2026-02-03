#!/bin/bash
set -e

REGISTRY=${REGISTRY:-gcr.io/PROJECT}
TAG=${TAG:-latest}

echo "Building frappe-siud image..."
docker build -t $REGISTRY/frappe-siud:$TAG \
  -f docker/frappe/Dockerfile \
  frappe_docker/development/frappe-bench/apps

echo "Building portal-ui image..."
docker build -t $REGISTRY/portal-ui:$TAG \
  -f docker/portal-ui/Dockerfile \
  supplier-portal-ui

echo "Pushing images..."
docker push $REGISTRY/frappe-siud:$TAG
docker push $REGISTRY/portal-ui:$TAG

echo "Done!"
