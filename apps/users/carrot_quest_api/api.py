from django.conf import settings
from django.utils import timezone

import json

import requests

import logging


logger = logging.getLogger('carrot_quest_order_completed')


class CarrotQuestAPI:
    BASE_URL = 'https://api.carrotquest.io/v1/'
    AUTH_TOKEN = settings.CARROT_REQUEST_AUTH_TOKEN

    # https://developers.carrotquest.io/endpoints/users/events/
    EVENTS_URL_PATH = 'users/{id}/events'
    EVENTS_URL = BASE_URL + EVENTS_URL_PATH + '?auth_token=' + AUTH_TOKEN

    # https://developers.carrotquest.io/endpoints/users/props/
    PROPS_URL_PATH = 'users/{id}/props'
    PROPS_URL = BASE_URL + PROPS_URL_PATH + '?auth_token=' + AUTH_TOKEN

    @classmethod
    def update_balance(cls, user_id: int, balance: int):
        operations = json.dumps([
            {"op": "update_or_create", "key": "balance", "value": balance}
        ])
        props_url = cls.PROPS_URL.format(id=user_id) + f'&by_user_id=true&operations={operations}'
        props_response = requests.post(props_url)
        if props_response.status_code != 200:
            logger.warning(f'order_completed.props. user: {user_id} - {props_response.json()}\n')

    @classmethod
    def order_completed(cls, user_id: int, data: dict):
        # создал заказ
        events_url = cls.EVENTS_URL.format(id=user_id) + \
                     f'&event=$order_completed&by_user_id=true&params={json.dumps(data)}'
        events_response = requests.post(events_url)

        if events_response.status_code != 200:
            logger.warning(f'\n{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}: order_completed.events. user: {user_id} - {events_response.json()}\n')
        operations = json.dumps([
            {"op": "add", "key": "$orders_count", "value": 1},
            {"op": "add", "key": "$revenue", "value": float(data["$order_amount"])},
            {"op": "update_or_create", "key": "$last_payment", "value": float(data["$order_amount"])}
        ])

        props_url = cls.PROPS_URL.format(id=user_id) + f'&by_user_id=true&operations={operations}'
        props_response = requests.post(props_url)
        if props_response.status_code != 200:
            logger.warning(f'order_completed.props. user: {user_id} - {props_response.json()}\n')

        # оплатил
        events_url = cls.EVENTS_URL.format(id=user_id) + \
                     f'&event=$order_paid&by_user_id=true&params={json.dumps(data)}'
        events_response = requests.post(events_url)
        if events_response.status_code != 200:
            logger.warning(f'\n{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}: order_paid.events. user: {user_id} - {events_response.json()}\n')
