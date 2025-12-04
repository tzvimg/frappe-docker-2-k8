#!/bin/bash
# Batch validate multiple YAML files
# Usage: ./scripts/batch_validate.sh <directory>

set -e

YAML_DIR=${1:-yaml_specs}
CONTAINER_NAME="frappe_docker_devcontainer-frappe-1"

echo "=========================================="
echo "Batch Validation"
echo "Directory: $YAML_DIR"
echo "=========================================="
echo ""

# Check if directory exists
if [ ! -d "$YAML_DIR" ]; then
  echo "Error: Directory not found: $YAML_DIR"
  exit 1
fi

# Check if container is running
if ! docker ps | grep -q $CONTAINER_NAME; then
  echo "Error: Container $CONTAINER_NAME is not running"
  echo "Please start the container first."
  exit 1
fi

# Find all YAML files
YAML_FILES=$(find "$YAML_DIR" -name "*.yaml" -o -name "*.yml")

if [ -z "$YAML_FILES" ]; then
  echo "No YAML files found in $YAML_DIR"
  exit 0
fi

TOTAL=0
PASSED=0
FAILED=0

# Validate each file
for file in $YAML_FILES; do
  TOTAL=$((TOTAL + 1))
  echo "[$TOTAL] Validating: $file"

  if docker exec $CONTAINER_NAME bash -c "
    cd /workspace/doctype_creator && \
    python validate_yaml.py /workspace/doctype_creator/$file
  " > /dev/null 2>&1; then
    echo "    ✓ PASSED"
    PASSED=$((PASSED + 1))
  else
    echo "    ✗ FAILED"
    FAILED=$((FAILED + 1))
  fi
  echo ""
done

echo "=========================================="
echo "BATCH VALIDATION SUMMARY"
echo "=========================================="
echo "Total files: $TOTAL"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
  echo "All validations passed!"
  exit 0
else
  echo "Some validations failed. Run individual validate.sh for details."
  exit 1
fi
