#!/bin/bash
# Open Frappe Python console
# Usage: ./console.sh

CONTAINER="frappe_docker_devcontainer-frappe-1"
SITE="development.localhost"
BENCH_DIR="/workspace/development/frappe-bench"

echo "Opening Python console for site: $SITE"
echo "Press Ctrl+D or type exit() to exit"
echo ""
docker exec -it "$CONTAINER" bash -c "cd $BENCH_DIR && bench --site $SITE console"
