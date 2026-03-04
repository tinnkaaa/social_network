FROM python:3.12-slim
# щоб не створювався .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# щоб логи одразу виводились
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
	gcc \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

RUN python manage.py makemigrations

RUN python manage.py migrate

ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=12345
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

RUN python manage.py createsuperuser --noinput

EXPOSE 8000

ENTRYPOINT [ "gunicorn", "core.wsgi", "-b", "0.0.0.0:8000" ]