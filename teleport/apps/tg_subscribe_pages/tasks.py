from __future__ import absolute_import, unicode_literals

from django.utils.timezone import datetime
from celery import shared_task

from .models import TelegramSubscribePage


@shared_task(name='calculate_and_save_telegram_ctr')
def calculate_and_save_ctr_telegram_ctr() -> None:
    subscribe_pages = TelegramSubscribePage.objects.filter(is_active=True, created=True)
    for subscribe_page in subscribe_pages:
        subscribe_page.save_ctr()

        statistics = subscribe_page.statistic.filter(day=datetime.today())
        for statistic in statistics:
            statistic.save_ctr()