#!/bin/bash
# Clear Frappe cache - run after DocType changes
# Usage: ./clear_cache.sh

CONTAINER="frappe_docker_devcontainer-frappe-1"
SITE="development.localhost"
BENCH_DIR="/workspace/development/frappe-bench"

echo "Clearing cache for site: $SITE"
docker exec "$CONTAINER" bash -c "cd $BENCH_DIR && bench --site $SITE clear-cache"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Cache cleared successfully"
else
    echo "✗ Failed to clear cache"
fi

exit $EXIT_CODE
