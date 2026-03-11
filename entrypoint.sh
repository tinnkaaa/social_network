#!/bin/bash
set -e

export DJANGO_SETTINGS_MODULE=core.settings

echo "Apply migrations"
python manage.py migrate --noinput

echo "Collect static"
python manage.py collectstatic --noinput

echo "Create superuser"

export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=12345
export DJANGO_SUPERUSER_EMAIL=admin@example.com

python manage.py createsuperuser --noinput || true

echo "Start Daphne"

exec daphne -b 0.0.0.0 -p ${PORT:-8000} core.asgi:application