#!/bin/bash
gunicorn -b 0.0.0.0:8000 -w $GUNICORN_WORKERS_AMOUNT getsub.wsgi:application & \
    celery -A getsub worker -l info & \
    celery -A getsub beat -l info
