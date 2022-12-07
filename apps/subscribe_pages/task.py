from django.utils.timezone import datetime

from getsub.celery import app


from .ispmanager_api.api import ISPManagerAPI
from .models import InstagramSubscribePage

import requests

import socket

import logging


loggerDomain = logging.getLogger('domain')


@app.task(name="save_instagram_info")
def save_instagram_info(n):
    pass


@app.task(name='calculate_and_save_ctr')
def calculate_and_save_ctr() -> None:
    subscribe_pages = InstagramSubscribePage.objects.filter(is_active=True, created=True)
    for subscribe_page in subscribe_pages:
        subscribe_page.save_ctr()

        statistics = subscribe_page.statistic.filter(day=datetime.today())
        for statistic in statistics:
            statistic.save_ctr()


@app.task(name='domain_add')
def domain_add(domain: str, try_: int = 1) -> None:
    try:
        ip = socket.gethostbyname(domain)
    except Exception as e:
        ip = None
        loggerDomain.warning(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: task_domain_add_get_ip: {domain} -- {try_} -- {e}\n')

    if ip == '62.109.7.205':
        ispmanager = ISPManagerAPI()
        response = ispmanager.add_webdomain(domain)
        if response.status_code != 200:
            loggerDomain.warning(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -- add_webdomain: {domain} - {response.json()}\n')
        response = ispmanager.add_cert(domain)
        if response.status_code != 200:
            loggerDomain.warning(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -- add_cert: {domain} - {response}\n')


@app.task(name='check_domain_cert')
def check_domain_cert(domain: str) -> None:
    try:
        requests.get(f'https://{domain}', verify=True)
    except requests.exceptions.SSLError:
        ispmanager = ISPManagerAPI()
        ispmanager.set_cert(domain)
    except requests.exceptions.ConnectionError:
        pass
