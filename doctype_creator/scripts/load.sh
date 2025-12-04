#!/bin/bash
# Convenience script to load DocType from host
# Usage: ./scripts/load.sh <yaml_file> [site]

set -e

YAML_FILE=$1
SITE=${2:-development.localhost}
CONTAINER_NAME="frappe_docker_devcontainer-frappe-1"

if [ -z "$YAML_FILE" ]; then
  echo "Usage: ./scripts/load.sh <yaml_file> [site]"
  echo ""
  echo "Examples:"
  echo "  ./scripts/load.sh yaml_specs/service_provider.yaml"
  echo "  ./scripts/load.sh yaml_specs/service_provider.yaml production.localhost"
  echo ""
  exit 1
fi

# Check if file exists
if [ ! -f "$YAML_FILE" ]; then
  echo "Error: File not found: $YAML_FILE"
  exit 1
fi

echo "=========================================="
echo "Loading DocType from: $YAML_FILE"
echo "Target site: $SITE"
echo "=========================================="
echo ""

# Check if container is running
if ! docker ps | grep -q $CONTAINER_NAME; then
  echo "Error: Container $CONTAINER_NAME is not running"
  echo "Please start the container first."
  exit 1
fi

# Execute load command
docker exec -it $CONTAINER_NAME bash -c "
  cd /workspace/development/frappe-bench && \
  python /workspace/doctype_creator/load_doctype.py \
    /workspace/doctype_creator/$YAML_FILE \
    --site $SITE && \
  echo '' && \
  echo 'Clearing cache...' && \
  bench --site $SITE clear-cache
"

if [ $? -eq 0 ]; then
  echo ""
  echo "=========================================="
  echo "SUCCESS!"
  echo "=========================================="
  echo "DocType loaded and cache cleared."
  echo "Access at: http://localhost:8000"
  echo ""
else
  echo ""
  echo "=========================================="
  echo "FAILED"
  echo "=========================================="
  echo "See error messages above for details."
  exit 1
fi
