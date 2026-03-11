#!/bin/bash

set -e

echo "Apply migrations"
python manage.py migrate --noinput

echo "Collect static"
python manage.py collectstatic --noinput

echo "Create admin if not exists"

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

username="admin"
password="12345"
email="admin@example.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username,email,password)
END

echo "Start Daphne"

exec daphne -b 0.0.0.0 -p 8000 core.asgi:application