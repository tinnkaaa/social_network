#!/bin/bash
set -e

# Встановлюємо налаштування Django
export DJANGO_SETTINGS_MODULE=core.settings

echo "Apply migrations..."
python manage.py migrate --settings=core.settings --noinput

echo "Collect static files..."
python manage.py collectstatic --settings=core.settings --noinput

echo "Create superuser if not exists..."
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=12345
export DJANGO_SUPERUSER_EMAIL=admin@example.com

# --noinput + || true щоб не падало, якщо юзер вже існує
python manage.py createsuperuser --settings=core.settings --noinput || true

echo "Starting Daphne..."
# Використовуємо динамічний порт Render
exec daphne -b 0.0.0.0 -p ${PORT:-8000} core.asgi:application