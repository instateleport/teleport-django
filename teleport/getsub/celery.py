from __future__ import absolute_import, unicode_literals
import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'getsub.settings')


app = Celery('getsub', result_expires=60)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'calculate_and_save_telegram_ctr': {
        'task': 'calculate_and_save_telegram_ctr',
        'schedule': 60 * 20
    },
    'calculate_and_save_ctr': {
        'task': 'calculate_and_save_ctr',
        'schedule': 60 * 20
    },
}