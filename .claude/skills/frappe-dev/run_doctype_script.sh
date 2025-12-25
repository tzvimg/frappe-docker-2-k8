#!/bin/bash
# Helper script to run DocType creation scripts with minimal command variation
# Usage: ./run_doctype_script.sh <subdirectory.module.function>
# Example: ./run_doctype_script.sh creation.create_all_entities.create_all_doctypes

# Configuration - change these if your setup differs
CONTAINER="frappe_docker_devcontainer-frappe-1"
SITE="development.localhost"
APP="siud"
MODULE_PATH="doctypes_loading"
BENCH_DIR="/workspace/development/frappe-bench"

# Help message
if [ -z "$1" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: $0 <subdirectory.module.function>"
    echo ""
    echo "Directory Structure:"
    echo "  creation/    - DocType and workflow creation scripts"
    echo "  test_data/   - Test data loading scripts"
    echo "  temp/        - Temporary/utility scripts"
    echo ""
    echo "Examples:"
    echo "  $0 creation.create_all_entities.create_all_doctypes"
    echo "  $0 creation.create_supplier_inquiry_workflow.create_all"
    echo "  $0 creation.create_supplier_inquiry_workflow.delete_all"
    echo "  $0 test_data.create_test_data.load_test_data"
    echo "  $0 temp.verify_workflow.verify"
    echo ""
    echo "Configuration:"
    echo "  Container: $CONTAINER"
    echo "  Site: $SITE"
    echo "  App: $APP"
    echo "  Module: $MODULE_PATH"
    exit 1
fi

# Build the full module path
FULL_PATH="$APP.$MODULE_PATH.$1"

echo "Running: bench --site $SITE execute $FULL_PATH"
echo "In container: $CONTAINER"
echo ""

# Execute the command in the container
docker exec "$CONTAINER" bash -c "cd $BENCH_DIR && bench --site $SITE execute $FULL_PATH"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✓ Command completed successfully"
    echo ""
    echo "Don't forget to clear cache if needed:"
    echo "  docker exec $CONTAINER bash -c 'cd $BENCH_DIR && bench --site $SITE clear-cache'"
else
    echo ""
    echo "✗ Command failed with exit code $EXIT_CODE"
fi

exit $EXIT_CODE
