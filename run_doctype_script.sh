#!/bin/bash
# Helper script to run DocType creation scripts with minimal command variation
# Usage: ./run_doctype_script.sh <module.function>
# Example: ./run_doctype_script.sh create_all_entities.create_all_doctypes

# Configuration - change these if your setup differs
CONTAINER="frappe_docker_devcontainer-frappe-1"
SITE="development.localhost"
APP="siud"
MODULE_PATH="doctypes_loading"
BENCH_DIR="/workspace/development/frappe-bench"

# Help message
if [ -z "$1" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: $0 <module.function>"
    echo ""
    echo "Examples:"
    echo "  $0 create_all_entities.create_all_doctypes"
    echo "  $0 create_supplier.create_supplier_doctype"
    echo "  $0 create_all_entities.delete_all_doctypes"
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
