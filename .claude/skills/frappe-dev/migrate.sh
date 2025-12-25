#!/bin/bash
# Run database migrations - run after DocType JSON changes
# Usage: ./migrate.sh

CONTAINER="frappe_docker_devcontainer-frappe-1"
SITE="development.localhost"
BENCH_DIR="/workspace/development/frappe-bench"

echo "Running migrations for site: $SITE"
docker exec "$CONTAINER" bash -c "cd $BENCH_DIR && bench --site $SITE migrate"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Migration completed successfully"
else
    echo "✗ Migration failed"
fi

exit $EXIT_CODE
