#!/bin/bash
gunicorn -b $GUNICORN_HOST:$GUNICORN_PORT -w $GUNICORN_WORKERS_AMOUNT getsub.wsgi:application & \
    celery -A getsub worker -l info & \
    celery -A getsub beat -l info
