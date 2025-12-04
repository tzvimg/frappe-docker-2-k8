#!/bin/bash
# Convenience script to inject Python controller into DocType

set -e  # Exit on error

DOCTYPE_NAME="$1"
CONTROLLER_FILE="$2"
APP="${3:-nursing_management}"

if [ -z "$DOCTYPE_NAME" ] || [ -z "$CONTROLLER_FILE" ]; then
  echo "Usage: ./scripts/inject.sh <doctype_name> <controller_file> [app]"
  echo ""
  echo "Arguments:"
  echo "  doctype_name     - Name of DocType (e.g., 'Service Provider')"
  echo "  controller_file  - Path to controller .py file"
  echo "  app             - App name (default: nursing_management)"
  echo ""
  echo "Examples:"
  echo "  ./scripts/inject.sh 'Service Provider' controllers/service_provider.py"
  echo "  ./scripts/inject.sh 'Contract' controllers/contract.py nursing_management"
  echo ""
  echo "Additional options (pass as environment variables):"
  echo "  NO_BACKUP=1      - Skip backup of existing controller"
  echo "  NO_VALIDATE=1    - Skip controller validation"
  echo ""
  echo "Examples with options:"
  echo "  NO_BACKUP=1 ./scripts/inject.sh 'Service Provider' controllers/service_provider.py"
  echo "  NO_VALIDATE=1 ./scripts/inject.sh 'Test DocType' controllers/test.py"
  exit 1
fi

# Build command arguments
CMD_ARGS=""
if [ ! -z "$NO_BACKUP" ]; then
  CMD_ARGS="$CMD_ARGS --no-backup"
fi

if [ ! -z "$NO_VALIDATE" ]; then
  CMD_ARGS="$CMD_ARGS --no-validate"
fi

echo "========================================"
echo "Controller Injection Script"
echo "========================================"
echo "DocType:    $DOCTYPE_NAME"
echo "Controller: $CONTROLLER_FILE"
echo "App:        $APP"
echo "Options:    ${CMD_ARGS:-none}"
echo "========================================"
echo ""

# Check if controller file exists
if [ ! -f "$CONTROLLER_FILE" ]; then
  echo "❌ Error: Controller file not found: $CONTROLLER_FILE"
  exit 1
fi

echo "Step 1: Injecting controller..."
echo ""

docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/doctype_creator && \
  python -m src.controller_injector '$DOCTYPE_NAME' /workspace/doctype_creator/$CONTROLLER_FILE --app $APP $CMD_ARGS
"

INJECT_STATUS=$?

if [ $INJECT_STATUS -ne 0 ]; then
  echo ""
  echo "❌ Controller injection failed!"
  exit $INJECT_STATUS
fi

echo ""
echo "Step 2: Clearing cache..."
docker exec -it frappe_docker_devcontainer-frappe-1 bash -c "
  cd /workspace/development/frappe-bench && \
  bench --site development.localhost clear-cache
"

echo ""
echo "========================================"
echo "✓ CONTROLLER INJECTION COMPLETE"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Restart Frappe: bench restart"
echo "  2. Test in UI: http://localhost:8000"
echo "  3. Check logs for any errors"
echo ""
echo "Useful commands:"
echo "  # List backups"
echo "  docker exec -it frappe_docker_devcontainer-frappe-1 bash -c \\"
echo "    'cd /workspace/doctype_creator && python -m src.controller_injector \"$DOCTYPE_NAME\" --list-backups --app $APP'"
echo ""
echo "  # Restore from backup"
echo "  docker exec -it frappe_docker_devcontainer-frappe-1 bash -c \\"
echo "    'cd /workspace/doctype_creator && python -m src.controller_injector \"$DOCTYPE_NAME\" --restore <backup_file> --app $APP'"
