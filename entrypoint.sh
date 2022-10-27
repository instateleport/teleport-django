#!/bin/bash
sleep 5
python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn -b 0.0.0.0:8000 -w 1 getsub.wsgi:application & \
    celery -A getsub worker -l info & \
    celery -A getsub beat -l info
