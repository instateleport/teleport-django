from typing import List, Optional, Union, Callable

from django.utils.translation import gettext_lazy as _
from django.utils.timezone import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, pre_save
from django.db import models
from django.contrib.postgres.fields import JSONField

from decimal import Decimal

from uuid import uuid4

import logging

# local imports
from apps.partners.models import Channel

from apps.subscribe_pages.models import (
    GroupOfSubscribePage,
    CostPerSubscriber, InstagramSubscribePage,

    VKGroupOfSubscribePage
)


class CustomUser(AbstractUser):
    AVATAR_CHOICES = (
        ('man', 'man'),
        ('woman', 'woman')
    )
    THEME_CHOICES = (
        ('white', 'white'),
        ('black', 'black')
    )

    def get_user_avatar_path(self, filename):
        return f'users/{self.id}/{filename}'

    def get_avatar_path(self, filename):
        return f'user/{self.username}/{filename}'

    email = models.EmailField(verbose_name=_('Email адрес'), blank=False,
                              unique=True)

    verification_uuid = models.UUIDField(default=uuid4,
                                         verbose_name=_('Верификационный UUID'))
    is_change_password = models.BooleanField(default=False)

    is_referral = models.BooleanField(default=False, verbose_name=_('Реферал'))
    referrer_channel = models.ForeignKey(Channel, on_delete=models.SET_NULL,
                                         null=True, blank=True,
                                         verbose_name=_('Канал пригласителя'))

    theme = models.CharField(max_length=15, choices=THEME_CHOICES,
                             default='white',
                             verbose_name=_('Тема'))

    phone = models.CharField(max_length=255, null=True, blank=True,
                             unique=True, verbose_name=_('Телефон'))

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователиаа'

    def generate_verification_uuid(self):
        self.verification_uuid = uuid4()
        self.save()
        return self.verification_uuid

    def __str__(self):
        return self.username


class Pocket(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                verbose_name=_('Пользователь'))
    balance = models.DecimalField(max_digits=10, decimal_places=2,
                                  blank=True, default=0, verbose_name=_('Баланс'))

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'

    def pay_per_subscriber(self) -> None:
        self.balance -= 1
        self.save(update_fields=['balance'])

    @property
    def balance_as_int(self):
        return int(self.balance)

    def __str__(self):
        return f'{self.balance}'


@receiver(post_save, sender=CustomUser)
def create_pocket_and_uuid(sender, created, instance, **kwargs):
    if created:
        Pocket.objects.create(user=instance, balance=Decimal(10))
        VKGroupOfSubscribePage.objects.get_or_create(
            user=instance,
            name=_('Неотсортированные'),
            can_delete=False
        )
        GroupOfSubscribePage.objects.get_or_create(
            user=instance,
            name=_('Неотсортированные'),
            can_delete=False
        )


@receiver(post_save, sender=Pocket)
def off_pages(sender, created, instance, **kwargs):
    user = instance.user
    if instance.balance <= 0:  # отключаем, если баланс кончился
        InstagramSubscribePage.deactivate_user_subscribe_pages(user)
    else:  # включаем, если есть баланс
        InstagramSubscribePage.activate_user_subscribe_pages(user)
