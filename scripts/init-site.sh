#!/bin/bash
set -e

SITE_NAME="${SITE_NAME:-siud.local}"
DB_HOST="${DB_HOST:-mariadb}"
DB_ROOT_PASSWORD="${DB_ROOT_PASSWORD:-frappe_root_pw}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin}"

cd /home/frappe/frappe-bench

# Wait for MariaDB
echo "Waiting for MariaDB..."
wait-for-it $DB_HOST:3306 -t 60

# Create common_site_config.json
cat > sites/common_site_config.json << EOF
{
  "db_host": "$DB_HOST",
  "redis_cache": "redis://redis-cache:6379",
  "redis_queue": "redis://redis-queue:6379",
  "redis_socketio": "redis://redis-queue:6379",
  "socketio_port": 9000,
  "serve_default_site": true,
  "default_site": "$SITE_NAME"
}
EOF

# Check if site exists
if [ ! -d "sites/$SITE_NAME" ]; then
    echo "Creating site $SITE_NAME..."
    bench new-site $SITE_NAME \
        --db-root-password $DB_ROOT_PASSWORD \
        --admin-password $ADMIN_PASSWORD \
        --no-mariadb-socket

    # Add siud to apps.txt if not present
    if ! grep -q "siud" sites/apps.txt 2>/dev/null; then
        echo "siud" >> sites/apps.txt
    fi

    echo "Installing siud app..."
    bench --site $SITE_NAME install-app siud

    echo "Site created successfully!"
else
    echo "Site $SITE_NAME already exists, running migrations..."
    bench --site $SITE_NAME migrate
fi

echo "Init complete."
