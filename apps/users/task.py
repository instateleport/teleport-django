from typing import Tuple, List, Union

from celery.schedules import timedelta

from time import sleep

from django.urls import reverse
from django.utils.timezone import datetime
from django.core.mail import send_mail
from django.conf import settings

# local imports
from getsub.celery import app

from .carrot_quest_api import CarrotQuestAPI
from .models import CustomUser


@app.task(name='reset_password')
def reset_password(email: Union[List[str], Tuple[str]]) -> None:
    email = email[0]
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return

    token = user.generate_verification_uuid()
    msg = f'Для восстановления пароля перейдите по ссылке ниже!\nhttps://instateleport.ru' \
          f'{reverse("users:verify", args=(token,))}'
    send_mail('verify', msg, settings.EMAIL_HOST_USER, [email], fail_silently=False)


@app.task(name='order_completed')
def order_completed(user_id: int, data: dict) -> None:
    CarrotQuestAPI.order_completed(user_id, data)


@app.task(name='carrot_quest_update_balance', rate_limit='3/s')
def carrot_quest_update_balance(user_id: int, balance: int) -> None:
    CarrotQuestAPI.update_balance(user_id, balance)
