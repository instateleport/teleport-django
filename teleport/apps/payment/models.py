from django.dispatch.dispatcher import receiver
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from uuid import uuid4, UUID

from decimal import Decimal

# local imports
from apps.users.models import CustomUser


class Order(models.Model):
    CURRENCY_CHOICES = (
        ('RUB', 'RUB'),
    )

    def account_generate(self) -> UUID:
        account = uuid4()
        if not Order.objects.filter(account=account):
            return account
        else:
            return self.account_generate()

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')

    unitpay_id = models.CharField(max_length=255, null=True, default=settings.UNITPAY_PUBLIC_KEY,
                                  verbose_name='UnitPay ID')
    project_id = models.CharField(max_length=255, null=True, default=settings.UNITPAY_PROJECT_ID,
                                  verbose_name='Project ID')

    # Order Info
    account = models.UUIDField(null=True, verbose_name='Идентификатор')
    description = models.CharField(max_length=150, verbose_name='Описание')
    order_sum = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Сумма')
    order_currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='RUB',
                                      verbose_name='Курс платежа')
    bonus = models.IntegerField(default=0, verbose_name='Бонус')

    paid = models.BooleanField(default=False, verbose_name='Оплачено')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def bonus_amount(self) -> Decimal:
        return (self.order_sum / 100) * self.bonus

    @property
    def full_amount(self) -> Decimal:
        return self.order_sum + self.bonus_amount

    def __str__(self):
        return f'{self.user}'


class OrderCent(models.Model):
    CURRENCY_CHOICES = (
        ('RUB', 'RUB'),
    )

    def order_id_generate(self) -> UUID:
        account = uuid4()
        if not Order.objects.filter(account=account):
            return account
        else:
            return self.order_id_generate()

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='cent_orders', verbose_name='Пользователь')

    # order info
    order_id = models.UUIDField(null=True, verbose_name='Идентификатор платежа')
    description = models.CharField(max_length=255, verbose_name='Описание')
    order_sum = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Сумма')
    order_currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='RUB', verbose_name='Курс')
    cent_bill_id = models.CharField(max_length=255, null=True)

    bonus = models.IntegerField(default=0, verbose_name='Бонус')

    paid = models.BooleanField(default=False, verbose_name='Оплачено')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Cent Заказ'
        verbose_name_plural = 'Cent Заказы'

    @property
    def bonus_amount(self) -> Decimal:
        return (self.order_sum / 100) * self.bonus

    @property
    def full_amount(self) -> Decimal:
        return self.order_sum + self.bonus_amount

    def __str__(self):
        return f'{self.user}'


@receiver(post_save, sender=Order)
def order_uuid_create(sender, created, instance: Order, **kwargs):
    if created:
        instance.account = instance.account_generate()
        instance.save(update_fields=['account'])


@receiver(post_save, sender=OrderCent)
def cent_order_uuid_create(sender, created, instance: OrderCent, **kwargs):
    if created:
        instance.order_id = instance.order_id_generate()
        instance.save(update_fields=['order_id'])

