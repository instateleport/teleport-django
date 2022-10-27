from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import gettext_lazy as _

from uuid import uuid4


class Partner(models.Model):
    referrer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partner',
                                    verbose_name=_('Пригласитель'))
    referrals = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='referrals', blank=True, verbose_name=_('Приглашённые'))

    percent = models.IntegerField(default=30, verbose_name=_('Отчисления'))

    earned = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_('Заработано'))
    clicks = models.IntegerField(default=0, verbose_name=_('Кликов'))

    active_referrals = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='active_referrals', blank=True,
                                              verbose_name=_('Активные пользователи'))

    def all_referrals_count(self):
        return self.referrals.count()
    all_referrals_count.short_description = 'Кол-во рефералов'

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'

    def __str__(self):
        return f'{self.referrer}'


class PartnerPocket(models.Model):
    partner = models.OneToOneField(Partner, on_delete=models.CASCADE, related_name='pocket', verbose_name=_('Партнёр'))

    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_('Баланс'))
    reserved = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_('Зарезервировано'))
    pay_outed = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_('Выплачено'))

    class Meta:
        verbose_name = 'Партнерский кошелек'
        verbose_name_plural = 'Партнерские кошельки'

    def __str__(self):
        return f'{self.partner}'


class Channel(models.Model):
    @classmethod
    def url_generate(cls):
        url = f'{uuid4().hex[:8]}'
        if cls.objects.filter(url=url):
            return cls.url_generate()
        return url

    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='channels', verbose_name=_('Пригласитель'))
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    url = models.CharField(max_length=255, null=True, verbose_name=_('Пригласительная ссылка'))

    clicks = models.IntegerField(default=0, verbose_name=_('Клики'))
    registered = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='registered', blank=True,
                                        verbose_name=_('Зарегистрировано'))

    earned = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Заработано'))

    can_delete = models.BooleanField(default=True, verbose_name=_('Возможно удалить'))

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'

    def registered_count(self):
        return self.registered.count()

    def __str__(self):
        return f'{self.partner} - {self.name}'


class Payout(models.Model):
    PAYMENT_CHOICES = (
        # ('qiwi', 'Киви'),
        ('yoomoney', 'Юmoney'),
        ('card', 'Карта'),
    )

    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='payouts', verbose_name=_('Пригласитель'))

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Сумма'))
    payment_type = models.CharField(max_length=255, choices=PAYMENT_CHOICES, verbose_name=_('Тип платежа'))
    payment_address = models.CharField(max_length=255, verbose_name=_('Адрес платежа'))

    is_pay_outed = models.BooleanField(default=False, verbose_name=_('Оплачено'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Создано'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Обновлено'))

    class Meta:
        verbose_name = 'Выплата'
        verbose_name_plural = 'Выплаты'

        ordering = ('-created', )

    def get_payment_type(self):
        return dict(self.PAYMENT_CHOICES).get(self.payment_type)

    def __str__(self):
        return f'{self.partner}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_partner(sender, created, instance, **kwargs):
    if created:
        partner = Partner.objects.create(referrer=instance)
        PartnerPocket.objects.create(partner=partner)
        Channel.objects.create(partner=partner, name='Основной', url=Channel.url_generate(), can_delete=False)


@receiver(post_save, sender=Payout)
def create_payout(sender, created, instance, **kwargs):
    pocket = instance.partner.pocket
    if instance.is_pay_outed:  # если платёж был выплачен
        pocket.reserved -= instance.amount
        pocket.pay_outed += instance.amount
    else:  # иначе (если создан)
        pocket.balance -= instance.amount
        pocket.reserved += instance.amount

    pocket.save(update_fields=['balance', 'reserved', 'pay_outed'])
