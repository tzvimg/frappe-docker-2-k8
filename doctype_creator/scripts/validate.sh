#!/bin/bash
# Convenience script to validate YAML file
# Usage: ./scripts/validate.sh <yaml_file>

set -e

YAML_FILE=$1
CONTAINER_NAME="frappe_docker_devcontainer-frappe-1"

if [ -z "$YAML_FILE" ]; then
  echo "Usage: ./scripts/validate.sh <yaml_file>"
  echo ""
  echo "Examples:"
  echo "  ./scripts/validate.sh yaml_specs/service_provider.yaml"
  echo "  ./scripts/validate.sh templates/examples/simple_doctype.yaml"
  echo ""
  exit 1
fi

# Check if file exists
if [ ! -f "$YAML_FILE" ]; then
  echo "Error: File not found: $YAML_FILE"
  exit 1
fi

echo "=========================================="
echo "Validating: $YAML_FILE"
echo "=========================================="
echo ""

# Check if container is running
if ! docker ps | grep -q $CONTAINER_NAME; then
  echo "Error: Container $CONTAINER_NAME is not running"
  echo "Please start the container first."
  exit 1
fi

# Execute validation
docker exec -it $CONTAINER_NAME bash -c "
  cd /workspace/doctype_creator && \
  python validate_yaml.py /workspace/doctype_creator/$YAML_FILE
"

if [ $? -eq 0 ]; then
  echo ""
  echo "=========================================="
  echo "VALIDATION PASSED"
  echo "=========================================="
  echo "The YAML file is valid and ready to load."
  echo ""
else
  echo ""
  echo "=========================================="
  echo "VALIDATION FAILED"
  echo "=========================================="
  echo "Please fix the errors shown above."
  exit 1
fi
