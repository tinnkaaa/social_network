#!/bin/bash
set -e

echo "Waiting for database and environment to be ready..."

# Міграції
echo "Apply migrations..."
python manage.py migrate --settings=core.settings --noinput

# Static файли
echo "Collect static files..."
python manage.py collectstatic --settings=core.settings --noinput

# Створення суперюзера
echo "Create superuser if not exists..."
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_PASSWORD=12345
export DJANGO_SUPERUSER_EMAIL=admin@example.com
python manage.py createsuperuser --settings=core.settings --noinput || true

# Запуск Daphne на динамічному порті Render
echo "Starting Daphne..."
exec daphne -b 0.0.0.0 -p ${PORT:-8000} core.asgi:application