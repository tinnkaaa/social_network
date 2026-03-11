#!/bin/bash
set -e

if [ "$RUN" = "gunicorn" ]; then
    exec gunicorn core.wsgi:application -b 0.0.0.0:8000
elif [ "$RUN" = "daphne" ]; then
    exec daphne -b 0.0.0.0 -p 10000 core.asgi:application
elif [ "$RUN" = "worker" ]; then
    exec celery -A core worker --loglevel=info
else
    echo "Specify RUN=gunicorn|daphne|worker"
    exit 1
fi