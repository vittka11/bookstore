#!/bin/sh

set -e

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Django with Gunicorn..."
exec "$@"