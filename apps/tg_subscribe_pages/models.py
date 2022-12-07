import hashlib
from typing import Optional
from typing import List

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.conf import settings
from django.dispatch.dispatcher import receiver
from django.utils.timezone import datetime
from django.db.models.signals import post_save

from apps.api.models import TelegramBotUser

from apps.subscribe_pages.models import BaseGroupOfSubscribePages
from apps.subscribe_pages.models import BaseSubscribePage
from apps.subscribe_pages.models import Domain
from apps.subscribe_pages.models import BGColor


class TelegramGroupOfSubscribePage(BaseGroupOfSubscribePages):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tg_group_of_pages',
        verbose_name=_('Владелец')
    )

    class Meta:
        verbose_name = 'Группа Telegram страницы'
        verbose_name_plural = 'Группы Telegram страниц'


class TelegramSubscribePage(BaseSubscribePage):
    def get_page_photo_path(self, filename: str) -> str:
        return f'subscribe_page/telegram-{self.user.username}/page_photos/{filename}'

    def get_instagram_avatar_path(self, filename: str) -> str:
        return f'subscribe_page/telegram-{self.user.username}/instagram_avatars/{filename}'

    @classmethod
    def slug_generate(cls, user: settings.AUTH_USER_MODEL, count: int=1):
        slug = f'tg-{user.username}-{cls.objects.filter(user=user).count() + count}'.replace(
            '.', '_')
        if cls.objects.filter(slug=slug):
            return cls.slug_generate(user, count + 1)
        return slug

    @classmethod
    def generate_page_hash(self, slug):
        page_hash = hashlib.sha256(slug.encode('utf-8')).hexdigest()[:10]
        return page_hash

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='tg_subscribe_pages',
        verbose_name=_('Пользователь')
    )
    group = models.ForeignKey(
        TelegramGroupOfSubscribePage,
        on_delete=models.SET_NULL,
        related_name='tg_subscribe_pages',
        null=True,
        blank=True,
        verbose_name=_('Группа страниц')
    )
    page_hash = models.CharField(
        max_length=200,
        unique=True
    )
    telegram_bot_url = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    telegram_user = models.ForeignKey(
        TelegramBotUser,
        on_delete=models.CASCADE,
        related_name='telegram_subscribe_pages',
        null=True,
        blank=True
    )
    telegram_channel_id = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    message_after_getting_present = models.CharField(
        max_length=2000,
        verbose_name=_('Сообщение при выдаче подарка')
    )
    button_text = models.CharField(
        max_length=500,
        default=_('ПОЛУЧИТЬ'),
        verbose_name=_('Текст на кнопке (бот)')
    )
    button_url = models.URLField(
        max_length=200,
        verbose_name=_('Ссылка кнопки (бот)'),
        null=True,
        blank=True
    )
    domain = models.ForeignKey(
        Domain,
        on_delete=models.SET_NULL,
        related_name='tg_subscribe_pages',
        blank=True,
        null=True,
        verbose_name=_('Домен')
    )
    page_photo = models.ImageField(
        upload_to=get_page_photo_path,
        blank=True,
        null=True,
        verbose_name=_('Page photo')
    )
    bg_color = models.ForeignKey(
        BGColor,
        related_name='tg_subscribe_pages',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Цвет фона')
    )
    instagram_username = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Имя в Telegram')
    )
    instagram_avatar = models.ImageField(
        upload_to=get_instagram_avatar_path,
        blank=True,
        null=True,
        verbose_name=_('Аватарка Telegram')
    )

    popup_title = models.CharField(
        max_length=50,
        verbose_name=_('Заголовок')
    )
    popup_button_text = models.CharField(
        max_length=19,
        default=_('ПОЛУЧИТЬ МАТЕРИАЛЫ'),
        verbose_name=_('Текст на кнопке (подписная страница)')
    )

    # Расширенные настройки
    presubscribe_text = models.CharField(
        max_length=255,
        default=_(
            'Подпишись на мой телеграм и '
            'ссылка для скачивания материалов станет доступна'
        ),
        verbose_name=_('Текст перед подпиской')
    )

    show_subscribers = models.BooleanField(default=False)

    following_count = models.CharField(
        max_length=12,
        blank=True,
        null=True
    )
    follower_count = models.CharField(
        max_length=12,
        blank=True,
        null=True
    )
    media_count = models.CharField(
        max_length=12,
        blank=True,
        null=True
    )
    is_linked = models.BooleanField(
        default=False,
        verbose_name=_('Привязан')
    )

    class Meta:
        verbose_name = 'Подписная Telegram страница'
        verbose_name_plural = 'Подписные Telegram страницы'

    def get_absolute_url(self) -> str:
        return reverse_lazy('subscribe_pages:page-detail', args=(self.slug,))

    def set_default_group(self):
        default_group, default_group_created = \
            TelegramGroupOfSubscribePage.objects.get_or_create(
                user=self.user, name='Неотсортированные'
            )
        self.group = default_group
        self.save(update_fields=['group'])

    def get_instagram_avatar_url(self) -> str:
        avatar_url = None
        if self.instagram_avatar:
            avatar_url = self.instagram_avatar.url

        if not avatar_url:
            if self.user.theme == 'white':
                avatar_url = '/media/images/icon/no_ava-white.svg'
            else:
                avatar_url = '/media/images/icon/no_ava.svg'
        return avatar_url

    @property
    def page_url(self) -> str:
        return f'{self.page_domain}/tg-page/{self.slug}'

    @property
    def page_domain(self) -> str:
        if self.domain:
            domain = self.domain.domain
        else:
            domain = settings.DOMAIN
        return domain

    def calculate_ctr(self) -> float:
        all_views, all_subscribers = \
            TelegramStatistic.get_all_views_and_subscribers(self)
        try:
            ctr = all_subscribers / all_views * 100
        except ZeroDivisionError:
            ctr = 0
        return ctr

    def all_views_subscribers_and_ctr(self) -> List[int]:
        all_views, all_subscribers = TelegramStatistic.get_all_views_and_subscribers(self)
        try:
            conversion = all_subscribers / all_views * 100
        except ZeroDivisionError:
            conversion = float()
        return [all_views, all_subscribers, conversion]

    all_views_subscribers_and_ctr.short_description = '👁‍🗨, 👤, %'

    @staticmethod
    def deactivate_user_subscribe_pages(user: settings.AUTH_USER_MODEL):
        for subscribe_page in user.tg_subscribe_pages.filter(is_active=True):
            subscribe_page.is_active = False
            subscribe_page.save(update_fields=['is_active'])

    @staticmethod
    def activate_user_subscribe_pages(user: settings.AUTH_USER_MODEL):
        for subscribe_page in user.tg_subscribe_pages.filter(is_active=False):
            subscribe_page.is_active = True
            subscribe_page.save(update_fields=['is_active'])


class TelegramStatistic(models.Model):
    telegram_subscribe_page = models.ForeignKey(
        TelegramSubscribePage,
        on_delete=models.CASCADE,
        verbose_name=_('Страница Telegram'),
        related_name='statistic'
    )
    day = models.DateField(verbose_name=_('Дата'))
    views = models.BigIntegerField(
        verbose_name=_('Просмотры'),
        default=0
    )
    subscribers = models.BigIntegerField(
        verbose_name=_('Подписки'),
        default=0
    )
    ctr = models.FloatField(
        default=0,
        blank=True,
        null=True,
        verbose_name=_('CTR')
    )

    class Meta:
        ordering = ('telegram_subscribe_page',)
        verbose_name = 'Статистика Telegram'
        verbose_name_plural = 'Статистики Telegram'

    @classmethod
    def get_all_views_and_subscribers(cls, subscribe_page: TelegramSubscribePage) -> List[int]:
        views, subscribers = 0, 0
        for statistic in cls.objects.filter(telegram_subscribe_page=subscribe_page):
            views += statistic.views
            subscribers += statistic.subscribers
        return [views, subscribers]

    def calculate_ctr(self) -> float:
        all_views_today, all_subscribers_today = self.views, self.subscribers
        print(all_subscribers_today, all_views_today)
        try:
            ctr = all_subscribers_today / all_views_today * 100
        except ZeroDivisionError:
            ctr = 0
        return ctr

    def save_ctr(self, ctr: Optional[float]=None) -> None:
        if not ctr:
            ctr = self.calculate_ctr()
        self.ctr = float('{:.2f}'.format(ctr))
        self.save(update_fields=['ctr'])

    def __str__(self):
        return f'{self.telegram_subscribe_page} - {self.day}'



class TelegramUser(models.Model):
    username = models.CharField(
        max_length=100
    )
    chat_id = models.CharField(
        max_length=100,
        unique=True
    )
    subscribe_to = models.ManyToManyField(
        TelegramSubscribePage,
        blank=True,
        related_name='subscribed_tg_users',
        verbose_name=_('Подписки')
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Время подписки')
    )


class TelegramSubscriber(models.Model):
    telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    ip = models.CharField(
        max_length=255,
        verbose_name=_('IP')
    )
    can_get_material = models.BooleanField(
        default=False,
        verbose_name=_('Может просматривать материал')
    )
    date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата')
    )
    views = models.ManyToManyField(
        TelegramSubscribePage,
        blank=True,
        related_name='views',
        verbose_name=_('Просмотры')
    )
    subscribe_to = models.ManyToManyField(
        TelegramSubscribePage,
        blank=True,
        related_name='subscribers',
        verbose_name=_('Подписки')
    )

    class Meta:
        verbose_name = 'Telegram Подписчик'
        verbose_name_plural = 'Telegram Подписчики'

    @classmethod
    def get_or_create_by_user_ip(cls, request=None, user_ip: str = None, username: str = None) -> 'TelegramSubscriber':
        if not user_ip and request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

            if x_forwarded_for:
                user_ip = x_forwarded_for.split(',')[0].strip()
            else:
                user_ip = request.META.get('REMOTE_ADDR').strip()
        try:
            subscriber, subscriber_created = cls.objects.get_or_create(
                ip=user_ip)  # получаем/создаём IP пользователя
        except cls.MultipleObjectsReturned:
            subscribers = cls.objects.filter(ip=user_ip)
            subscriber = subscribers[0]
            for subscriber_ in subscribers[1:]:
                for subscribe_page in subscriber_.views.all():
                    subscriber.views.add(subscribe_page)
                for subscribe_page in subscriber_.subscribe_to.all():
                    subscriber.subscribe_to.add(subscribe_page)
                subscriber_.delete()
        return subscriber

    def is_visited_page_by_slug(self, slug: str) -> bool:
        return self.views.filter(slug=slug)


@receiver(post_save, sender=TelegramSubscribePage)
def tg_subscribe_page_post_save(sender, created, instance: TelegramSubscribePage, **kwargs):
    print(777)
    if created:
        TelegramStatistic.objects.create(
            telegram_subscribe_page=instance, day=datetime.today()
        )
        default_group, default_group_created = TelegramGroupOfSubscribePage.objects.get_or_create(
            user=instance.user, name='Неотсортированные'
        )
        instance.group = default_group
        instance.slug = instance.slug.lower()
        instance.created = True

        instance.save(
            update_fields=[
                'slug',
                'created',
                'group'
            ]
        )
        # если баланс больше 0, то подписная страница становится активной
        if instance.user.pocket.balance > 0:
            instance.is_active = True
            instance.save(update_fields=['is_active'])