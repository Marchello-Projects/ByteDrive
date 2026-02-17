#!/bin/sh

set -e

echo "Waiting for postgres..."

while ! python -c "import socket; import sys; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); sys.exit(0 if s.connect_ex(('db', 5432)) == 0 else 1)"; do
  sleep 1
done

echo "PostgreSQL started"

echo "Applying database migrations..."
python manage.py migrate

echo "Starting server..."
exec "$@"