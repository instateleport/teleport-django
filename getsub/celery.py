from celery import Celery

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'getsub.settings')


app = Celery('getsub', result_expires=60)
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()
