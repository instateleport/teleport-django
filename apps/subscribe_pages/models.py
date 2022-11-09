from typing import List, Optional

from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import datetime
from django.urls import reverse_lazy
from django.conf import settings

from decimal import Decimal

import logging

ipLogger = logging.getLogger('ip')


class CostPerSubscriber(models.Model):
    price = models.DecimalField(max_digits=4, decimal_places=2,
                                verbose_name=_('Цена'))

    class Meta:
        verbose_name = 'Стоимость за одну подписку'
        verbose_name_plural = 'Стоимость за одну подписку'

    @classmethod
    def get_cost_per_subscriber(cls) -> Decimal:
        return cls.objects.first().price

    def __str__(self):
        return str(self.price)


class Domain(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='domains',
                             verbose_name=_('Пользователь'))
    domain = models.CharField(max_length=255, verbose_name=_('Домен'))
    for_delete = models.BooleanField(default=False)
    ssl = models.BooleanField(default=False, verbose_name=_('SSL сертификат'))
    is_active = models.BooleanField(default=False, verbose_name=_('Активный'))

    class Meta:
        verbose_name = 'Домен'
        verbose_name_plural = 'Домены'

    @classmethod
    def get_domains(cls):
        return ' '.join(set([domain.domain for domain in cls.objects.all() if
                             not domain.added]))

    def __str__(self):
        return self.domain


class BGColor(models.Model):
    slug = models.SlugField(max_length=255, verbose_name=_('Название цвета'))

    # страница
    first_color = models.CharField(max_length=50, verbose_name=_('Первый цвет'))
    second_color = models.CharField(max_length=50, verbose_name=_('Второй цвет'))
    text_color = models.CharField(max_length=50, default='#fff',
                                  verbose_name=_('Цвет текста'))

    # панель
    panel = models.CharField(max_length=50, default='#2C3955',
                             verbose_name=_('Цвет панели'))
    panel_text_color = models.CharField(max_length=50, default='#68A4FF',
                                        verbose_name=_('Цвет текста на панели'))
    panel_icon_color = models.CharField(max_length=50, default='#68A4FF',
                                        verbose_name=_('Цвет иконки на панели'))
    panel_icon_bg_color = models.CharField(max_length=50, default='#68A4FF45',
                                           verbose_name=_('Фон иконки'))

    # поле ввода
    input_bg_color = models.CharField(max_length=50, default='#272C44',
                                      verbose_name=_('Фон инпута'))
    input_text_color = models.CharField(max_length=50, default='#7088AC',
                                        verbose_name=_('Цвет текста инпута'))

    is_active = models.BooleanField(default=True, verbose_name=_('Активный'))

    class Meta:
        verbose_name = 'Цвет фона'
        verbose_name_plural = 'Цвета фона'

    @classmethod
    def get_default_bg_color(cls):
        return cls.objects.get(slug='default')

    def __str__(self):
        return f'{self.slug} : {self.first_color} - {self.second_color}'


class GroupOfSubscribePage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='group_of_pages',
                             verbose_name=_('Владелец'))
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Создано'))
    can_delete = models.BooleanField(default=True,
                                     verbose_name=_('Можно удалить'))

    class Meta:
        verbose_name = 'Группа страниц'
        verbose_name_plural = 'Группы страниц'

    def __str__(self):
        return f'{self.name}-{self.user}'


class InstagramSubscribePage(models.Model):
    def get_page_photo_path(self, filename: str) -> str:
        return f'subscribe_page/{self.instagram_username}/page_photos/{filename}'

    def get_instagram_avatar_path(self, filename: str) -> str:
        return f'subscribe_page/{self.instagram_username}/instagram_avatars/{filename}'

    @classmethod
    def slug_generate(cls, user: settings.AUTH_USER_MODEL, count: int = 1):
        slug = f'{user.username}-{cls.objects.filter(user=user).count() + count}'.replace(
            '.', '_')
        if cls.objects.filter(slug=slug):
            return cls.slug_generate(user, count + 1)
        return slug

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='subscribe_pages',
        verbose_name=_('Пользователь')
    )
    group = models.ForeignKey(
        GroupOfSubscribePage, on_delete=models.SET_NULL,
        related_name='subscribe_pages',
        null=True, blank=True,
        verbose_name=_('Группа страниц')
    )
    domain = models.ForeignKey(
        Domain, on_delete=models.SET_NULL,
        related_name='subscribe_pages',
        blank=True, null=True,
        verbose_name=_('Домен')
    )
    page_name = models.CharField(
        max_length=60,
        verbose_name=_('Название страницы')
    )
    slug = models.SlugField(
        max_length=30, db_index=True, unique=True,
        verbose_name=_('Ссылка подписной страницы')
    )
    page_photo = models.ImageField(
        upload_to=get_page_photo_path,
        blank=True, null=True,
        verbose_name=_('Page photo')
    )
    bg_color = models.ForeignKey(
        BGColor, related_name='subscribe_pages',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Цвет фона')
    )

    title = models.CharField(
        max_length=60, null=True,
        verbose_name=_('Заголовок')
    )
    description = models.TextField(
        null=True,
        verbose_name=_('Описание')
    )
    button_text = models.CharField(
        max_length=30,
        default=_('ПОЛУЧИТЬ'),
        verbose_name=_('Текст на кнопке')
    )

    instagram_username = models.CharField(
        max_length=40, null=True,
        verbose_name=_('Ник в Instagram')
    )
    instagram_name = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name=_('Имя в Instagram')
    )
    instagram_avatar = models.ImageField(
        upload_to=get_instagram_avatar_path,
        blank=True, null=True,
        verbose_name=_('Аватарка Instagram')
    )

    timer_text = models.CharField(
        max_length=39, blank=True, null=True,
        default=_('Материал станет недоступным через:'),
        verbose_name=_('Текст на таймере')
    )
    is_timer_active = models.BooleanField(
        default=False,
        verbose_name=_('Таймер обратного отсчёта')
    )
    timer_time = models.IntegerField(
        default=180,
        verbose_name=_('Время таймера (в секундах)')
    )

    facebook_pixel = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('Facebook пиксель')
    )
    tiktok_pixel = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('Tiktok пиксель')
    )
    vk_pixel = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('ВК пиксель')
    )
    yandex_pixel = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('Яндекс метрика')
    )
    roistat_id = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('Roistat ID')
    )

    ctr = models.FloatField(
        default=0, blank=True, null=True,
        verbose_name=_('CTR')
    )

    popup_title = models.CharField(
        max_length=50,
        default=_('Успешно'),
        verbose_name=_('Заголовок')
    )
    popup_text = models.TextField(
        default=_('Можете получить материалы, нажав по кнопке ниже.'),
        verbose_name=_('Текст'))
    popup_button_url = models.TextField(
        null=True,
        verbose_name=_('Ссылка кнопки')
    )
    popup_button_text = models.CharField(
        max_length=19,
        default=_('ПОЛУЧИТЬ МАТЕРИАЛЫ'),
        verbose_name=_('Текст на кнопке')
    )

    # Расширенные настройки
    presubscribe_text = models.CharField(
        max_length=255,
        default=_(
            'Подпишись на мой инстаграм и '
            'ссылка для скачивания материалов станет доступна'
        ),
        verbose_name=_('Текст перед подпиской')
    )
    precheck_subscribe_text = models.CharField(
        max_length=255,
        default=_('Введите ваш логин инстаграма для проверки подписки'),
        verbose_name=_(
            'Текст "Введите ваш логин инстаграма для проверки подписки"')
    )

    enter_login_placeholder = models.CharField(
        max_length=255,
        default=_('введите ваш логин'),
        verbose_name=_('Текст "Введите ваш логин"')
    )
    help_text = models.CharField(
        max_length=255,
        default=_('Здесь находится логин'),
        verbose_name=_('Текст "Здесь находиться логин" (подсказка)')
    )

    subscribe_button = models.CharField(
        max_length=255,
        default=_('Подписаться'),
        verbose_name=_('Текст "Подписаться" на кнопке')
    )
    already_subscribed_text = models.CharField(
        max_length=255,
        default=_('Я уже подписался'),
        verbose_name=_('Текст "Я уже подписался" под кнопкой')
    )

    subscribed_button = models.CharField(
        max_length=255,
        default=_('Подписался'),
        verbose_name=_('Текст "Я подписался" на кнопке')
    )
    not_yet_subscribed = models.CharField(
        max_length=255,
        default=_('Я еще не подписался'),
        verbose_name=_('Текст "Я еще не подписался" под кнопкой')
    )

    presearch_text = models.CharField(
        max_length=255,
        default=_('После подписки вернись на эту страницу для подтверждения'),
        verbose_name=_(
            'Текст "После подписки вернись на эту страницу для подтверждения"'
        )
    )
    search_text = models.CharField(
        max_length=255,
        default=_('Поиск аккаунта...'),
        verbose_name=_('Текст "Поиск аккаунта..."')
    )
    search_time_text = models.CharField(
        max_length=255,
        default=_('Это может занять до 20 секунд'),
        verbose_name=_('Текст "Это может занять до 20 секунд"')
    )
    success_text = models.CharField(
        max_length=255,
        default=_('Аккаунт найден!'),
        verbose_name=_('Текст "Аккаунт найден"')
    )
    error_text = models.CharField(
        max_length=255,
        default=_('Аккаунт не найден!'),
        verbose_name=_('Текст "Аккаунт не найден"')
    )

    single_page = models.BooleanField(default=False)
    show_subscribers = models.BooleanField(default=False)

    following_count = models.CharField(max_length=12, blank=True, null=True)
    follower_count = models.CharField(max_length=12, blank=True, null=True)
    media_count = models.CharField(max_length=12, blank=True, null=True)

    is_active = models.BooleanField(default=False, verbose_name=_('Активный'))
    created = models.BooleanField(default=False, verbose_name=_('Создано'))

    class Meta:
        verbose_name = 'Подписная страница'
        verbose_name_plural = 'Подписные страницы'

    def get_absolute_url(self) -> str:
        return reverse_lazy('subscribe_pages:page-detail', args=(self.slug,))

    def get_page_photo_url(self) -> str:
        if self.page_photo:
            return f'{settings.DOMAIN}{self.page_photo.url}' 
        return '#'

    def set_default_group(self):
        default_group, default_group_created = \
            GroupOfSubscribePage.objects.get_or_create(
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
        return f'{self.page_domain}/page/{self.slug}'

    @property
    def page_domain(self) -> str:
        if self.domain:
            domain = self.domain.domain
        else:
            domain = settings.DOMAIN
        return domain

    def calculate_ctr(self) -> float:
        all_views, all_subscribers = \
            InstagramStatistic.get_all_views_and_subscribers(self)
        try:
            ctr = all_subscribers / all_views * 100
        except ZeroDivisionError:
            ctr = 0
        return ctr

    def save_ctr(self, ctr: Optional[float] = None) -> None:
        if not ctr:
            ctr = self.calculate_ctr()
        self.ctr = float('{:.2f}'.format(ctr))
        self.save(update_fields=['ctr'])

    def all_views_subscribers_and_ctr(self) -> List[int]:
        all_views, all_subscribers = InstagramStatistic.get_all_views_and_subscribers(
            self)
        return [all_views, all_subscribers, self.ctr]

    all_views_subscribers_and_ctr.short_description = '👁‍🗨, 👤, %'

    @staticmethod
    def deactivate_user_subscribe_pages(user: settings.AUTH_USER_MODEL):
        for subscribe_page in user.subscribe_pages.filter(is_active=True):
            subscribe_page.is_active = False
            subscribe_page.save(update_fields=['is_active'])

    @staticmethod
    def activate_user_subscribe_pages(user: settings.AUTH_USER_MODEL):
        for subscribe_page in user.subscribe_pages.filter(is_active=False):
            subscribe_page.is_active = True
            subscribe_page.save(update_fields=['is_active'])

    @classmethod
    def is_slug_unique(cls, slug) -> bool:
        return not cls.objects.filter(slug=slug)

    def __str__(self):
        return f'{self.page_name} - {self.slug}'


class InstagramStatistic(models.Model):
    subscribe_page = models.ForeignKey(InstagramSubscribePage,
                                       on_delete=models.CASCADE,
                                       verbose_name=_('Страница'),
                                       related_name='statistic')
    day = models.DateField(verbose_name=_('Дата'))
    views = models.BigIntegerField(verbose_name=_('Просмотры'), default=0)
    subscribers = models.BigIntegerField(verbose_name=_('Подписки'), default=0)
    ctr = models.FloatField(default=0, blank=True, null=True,
                            verbose_name=_('CTR'))

    class Meta:
        ordering = ('subscribe_page',)
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистики'

    @classmethod
    def get_all_views_and_subscribers(cls,
                                      subscribe_page: InstagramSubscribePage) -> \
            List[int]:
        views, subscribers = 0, 0
        for statistic in cls.objects.filter(subscribe_page=subscribe_page):
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

    def save_ctr(self, ctr: Optional[float] = None) -> None:
        if not ctr:
            ctr = self.calculate_ctr()
        self.ctr = float('{:.2f}'.format(ctr))
        self.save(update_fields=['ctr'])

    def __str__(self):
        return f'{self.subscribe_page} - {self.day}'


class InstagramSubscriber(models.Model):
    ip = models.CharField(max_length=255, verbose_name=_('IP'))
    instagram_username = models.CharField(max_length=255, null=True,
                                          blank=True,
                                          verbose_name=_('Ник в Instagram'))

    can_get_material = models.BooleanField(
        default=False, verbose_name=_('Может просматривать материал'))
    date = models.DateTimeField(auto_now=True, verbose_name=_('Дата'))

    views = models.ManyToManyField(InstagramSubscribePage, blank=True,
                                   related_name='views',
                                   verbose_name=_('Просмотры'))
    subscribe_to = models.ManyToManyField(InstagramSubscribePage, blank=True,
                                          related_name='subscribers',
                                          verbose_name=_('Подписки'))

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    @classmethod
    def get_or_create_by_user_ip(cls, request=None, user_ip: str = None,
                                 username: str = None) -> 'InstagramSubscriber':
        if not user_ip and request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            # ipLogger.info(
            #     f'\n{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}: username: {username}, ip: {x_forwarded_for}')

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
        # if username:
        #     if subscriber.instagram_username != username:
        #         subscriber.instagram_username = username
        #         subscriber.save(update_fields=['instagram_username'])
        return subscriber

    def is_visited_page_by_slug(self, slug: str) -> bool:
        self.views.filter()
        return self.views.filter(slug=slug)

    def __str__(self):
        return f'{self.ip}-{self.instagram_username}'


class InstagramCreator(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='instagrams',
                             verbose_name=_('User'), null=True)
    instagram = models.CharField(max_length=250, verbose_name=_('Instagram'))

    class Meta:
        verbose_name = 'Instagram пользователя'
        verbose_name_plural = 'Instagram пользователей'

    def __str__(self):
        return self.instagram


# VK
class VKGroupOfSubscribePage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='vk_group_of_pages',
                             verbose_name=_('Владелец'))
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Создано'))
    can_delete = models.BooleanField(default=True,
                                     verbose_name=_('Можно удалить'))

    class Meta:
        verbose_name = 'Группа ВК страницы'
        verbose_name_plural = 'Группы ВК страниц'

    def __str__(self):
        return f'{self.name}-{self.user}'


class VKSubscribePage(models.Model):
    def get_page_photo_path(self, filename: str) -> str:
        return f'vk_subscribe_page/{self.slug}/{filename}'

    @classmethod
    def slug_generate(cls, user: settings.AUTH_USER_MODEL, count: int = 1):
        slug = (
            f'{user.username}-'
            f'{cls.objects.filter(user=user).count() + count}'
        ).replace('.', '_')
        if cls.objects.filter(slug=slug):
            return cls.slug_generate(user, count + 1)
        return slug

    TYPE_GROUP_ID_CHOICES = (
        ('id', 'id'),
        ('slug', 'slug')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='vk_subscribe_pages',
                             verbose_name=_('Пользователь'))
    group = models.ForeignKey(
        VKGroupOfSubscribePage, on_delete=models.SET_NULL,
        related_name='vk_subscribe_pages', null=True, blank=True,
        verbose_name=_('Группа ВК страниц'))
    page_name = models.CharField(max_length=60,
                                 verbose_name=_('Название страницы'))
    slug = models.SlugField(max_length=30, db_index=True, unique=True,
                            verbose_name=_('Ссылка подписной страницы'))
    page_photo = models.ImageField(upload_to=get_page_photo_path, blank=True,
                                   null=True, verbose_name=_('Page photo'))
    bg_color = models.ForeignKey(BGColor, related_name='vk_subscribe_pages',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 verbose_name=_('Цвет фона'))

    title = models.CharField(max_length=60, null=True,
                             verbose_name=_('Заголовок'))
    description = models.TextField(null=True, verbose_name=_('Описание'))
    button_text = models.CharField(max_length=30, default='ПОЛУЧИТЬ',
                                   verbose_name=_('Текст на кнопке'))

    vk_group_id = models.CharField(max_length=70, null=True,
                                   verbose_name=_('ID группы ВК'))
    type_group_id = models.CharField(max_length=10, default='id',
                                     choices=TYPE_GROUP_ID_CHOICES,
                                     verbose_name=_('Тип id группы'))

    timer_text = models.CharField(max_length=39,
                                  default='Материал станет недоступным через:',
                                  blank=True, null=True,
                                  verbose_name=_('Текст на таймере'))
    is_timer_active = models.BooleanField(
        default=False, verbose_name=_('Таймер обратного отсчёта'))
    timer_time = models.IntegerField(default=180,
                                     verbose_name=_('Время таймера (в секундах)'))

    facebook_pixel = models.CharField(max_length=255, blank=True, null=True,
                                      verbose_name=_('Facebook пиксель'))
    tiktok_pixel = models.CharField(max_length=255, blank=True, null=True,
                                    verbose_name=_('Tiktok пиксель'))
    vk_pixel = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name=_('ВК пиксель'))
    yandex_pixel = models.CharField(max_length=255, blank=True, null=True,
                                    verbose_name=_('Яндекс метрика'))
    roistat_id = models.CharField(max_length=255, blank=True, null=True,
                                  verbose_name=_('Roistat ID'))

    ctr = models.FloatField(default=0, blank=True, null=True,
                            verbose_name=_('CTR'))

    success_title = models.CharField(max_length=50, default='Успешно',
                                     verbose_name=_('Заголовок'))
    success_text = models.TextField(
        default='Можете получить материалы, нажав по кнопке ниже.',
        verbose_name=_('Текст'))
    success_button_url = models.TextField(null=True,
                                          verbose_name=_('Ссылка кнопки'))
    success_button_text = models.CharField(max_length=19,
                                           default='ПОЛУЧИТЬ МАТЕРИАЛЫ',
                                           verbose_name=_('Текст на кнопке'))

    is_active = models.BooleanField(default=False, verbose_name=_('Активный'))
    created = models.BooleanField(default=False, verbose_name=_('Создано'))

    class Meta:
        verbose_name = 'ВК Подписная страница'
        verbose_name_plural = 'ВК Подписные страницы'

    def get_absolute_url(self) -> str:
        return reverse_lazy('subscribe_pages:vk_page-detail',
                            args=(self.slug,))

    def get_page_photo_url(self) -> str:
        if self.page_photo:
            return f'{settings.DOMAIN}{self.page_photo.url}'
        return '#'

    @property
    def page_url(self) -> str:
        # return f'https://{self.page_domain}/vk-page/{self.slug}'
        return f'https://vk.com/app51446451#{self.slug}'

    def calculate_ctr(self) -> float:
        all_views, all_subscribers = \
            VKStatistic.get_all_views_and_subscribers(self)
        try:
            ctr = all_subscribers / all_views * 100
        except ZeroDivisionError:
            ctr = 0
        return round(ctr, 2)

    def save_ctr(self, ctr: Optional[float] = None) -> None:
        if not ctr:
            ctr = self.calculate_ctr()
        self.ctr = float('{:.2f}'.format(ctr))
        self.save(update_fields=['ctr'])

    def all_views_subscribers_and_ctr(self) -> List[int]:
        page_subscriptions = self.subscriptions.all()

        views = page_subscriptions.count()
        subscribers = page_subscriptions.filter(subscribed=True).count()
        try:
            ctr = round(subscribers / views * 100, 2)
        except ZeroDivisionError:
            ctr = 0
        return [views, subscribers, ctr]

    all_views_subscribers_and_ctr.short_description = '👁‍🗨, 👤, %'

    @staticmethod
    def deactivate_user_vk_subscribe_pages(user: settings.AUTH_USER_MODEL):
        for vk_subscribe_page in user.vk_subscribe_pages.filter(
                is_active=True):
            vk_subscribe_page.is_active = False
            vk_subscribe_page.save(update_fields=['is_active'])

    @staticmethod
    def activate_user_vk_subscribe_pages(user: settings.AUTH_USER_MODEL):
        for subscribe_page in user.subscribe_pages.filter(is_active=False):
            subscribe_page.is_active = True
            subscribe_page.save(update_fields=['is_active'])

    @classmethod
    def is_slug_unique(cls, slug) -> bool:
        return not cls.objects.filter(slug=slug)

    @property
    def bg_first_color(self):
        return self.bg_color.first_color

    @property
    def bg_second_color(self):
        return self.bg_color.second_color

    @property
    def text_color(self):
        return self.bg_color.text_color

    @property
    def panel_bg_color(self):
        return self.bg_color.panel

    @property
    def panel_text_color(self):
        return self.bg_color.panel_text_color

    @property
    def panel_icon_color(self):
        return self.bg_color.panel_icon_color

    def __str__(self):
        return f'{self.page_name} - {self.slug}'


class VKStatistic(models.Model):
    vk_subscribe_page = models.ForeignKey(VKSubscribePage,
                                          on_delete=models.CASCADE,
                                          verbose_name=_('ВК Страница'),
                                          related_name='statistic')
    day = models.DateField(verbose_name=_('Дата'))
    views = models.BigIntegerField(verbose_name=_('Просмотры'), default=0)
    subscribers = models.BigIntegerField(verbose_name=_('Подписки'), default=0)
    ctr = models.FloatField(default=0, blank=True, null=True,
                            verbose_name=_('CTR'))

    class Meta:
        ordering = ('vk_subscribe_page',)
        verbose_name = 'ВК Статистика'
        verbose_name_plural = 'ВК Статистики'

    @classmethod
    def get_all_views_and_subscribers(cls,
                                      vk_subscribe_page: VKSubscribePage) -> \
            List[int]:
        views, subscribers = 0, 0
        for statistic in cls.objects.filter(
                vk_subscribe_page=vk_subscribe_page):
            views += statistic.views
            subscribers += statistic.subscribers
        return [views, subscribers]

    def calculate_ctr(self) -> float:
        all_views_today, all_subscribers_today = self.views, self.subscribers
        try:
            ctr = all_subscribers_today / all_views_today * 100
        except ZeroDivisionError:
            ctr = 0
        return ctr

    def save_ctr(self, ctr: Optional[float] = None) -> None:
        if not ctr:
            ctr = self.calculate_ctr()
        self.ctr = float('{:.2f}'.format(ctr))
        self.save(update_fields=['ctr'])

    def __str__(self):
        return f'{self.vk_subscribe_page} - {self.day}'


class VKSubscriber(models.Model):
    """
    {
      "type": "VKWebAppGetUserInfoResult",
      "data": {
        "id": 2314852,
        "first_name": "Ирина",
        "last_name": "Денежкина",
        "sex": 1,
        "city": {
          "id": 2,
          "title": "Санкт-Петербург"
        },
        "country": {
          "id": 1,
          "title": "Россия"
        },
        "bdate": "10.4.1990",
        "photo_100": "https://pp.userapi.com/c836333/v836333553/5b138/2eWBOuj5A4g.jpg]",
        "photo_200": "https://pp.userapi.com/c836333/v836333553/5b137/tEJNQNigU80.jpg]",
        "timezone": 3
      }
    }
    """
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    vk_user_id = models.BigIntegerField(verbose_name=_('ID пользователя ВК'),
                                        unique=True)

    first_name = models.CharField(max_length=255, null=True, blank=True,
                                  verbose_name=_('Имя'))
    last_name = models.CharField(max_length=255, null=True, blank=True,
                                 verbose_name=_('Фамиллия'))
    sex = models.IntegerField(null=True, blank=True, verbose_name=_('Пол'))

    photo = models.CharField(max_length=255, null=True, blank=True,
                             verbose_name=_('Фото'))

    country = models.CharField(max_length=255, null=True, blank=True,
                               verbose_name=_('Страна'))
    birthday = models.CharField(max_length=255, null=True, blank=True,
                                verbose_name=_('День рождения'))
    date = models.DateTimeField(auto_now=True,
                                verbose_name=_('Дата создания в сервисе'))

    class Meta:
        verbose_name = 'ВК Подписчик'
        verbose_name_plural = 'ВК Подписчики'

    def __str__(self):
        return f'{self.id} - {self.first_name}'


class VKSubscription(models.Model):
    vk_subscriber = models.ForeignKey(VKSubscriber, on_delete=models.CASCADE,
                                      related_name='subscriptions',
                                      verbose_name=_('ВК подписчик'))
    vk_page = models.ForeignKey(VKSubscribePage, on_delete=models.CASCADE,
                                related_name='subscriptions',
                                verbose_name=_('ВК подписная страница'))

    subscribed = models.BooleanField(default=False, verbose_name=_('Подписался'))
    date = models.DateTimeField(null=True, auto_now_add=True,
                                verbose_name=_('Дата подписки'))

    class Meta:
        verbose_name = 'ВК Подписка'
        verbose_name_plural = 'ВК Подписки'
        unique_together = ('vk_subscriber', 'vk_page')

    def pay_per_subscriber(self):
        return self.vk_page.user.pocket.pay_per_subscriber()

    def subscribe(self) -> None:
        self.subscribed = True
        self.save(update_fields=['subscribed'])

    def __str__(self):
        return f'{self.vk_subscriber} - {self.vk_page.slug}'


class TelegramUser(models.Model):
    telegram_username = models.CharField(max_length=100)
    telegram_user_id = models.CharField(max_length=100)

    def __str__(self):
        return self.telegram_username


class TelegramGroupOfSubscribePage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='tg_group_of_pages',
                             verbose_name=_('Владелец'))
    name = models.CharField(max_length=255, verbose_name=_('Название'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Создано'))
    can_delete = models.BooleanField(default=True,
                                     verbose_name=_('Можно удалить'))

    class Meta:
        verbose_name = 'Группа Telegram страницы'
        verbose_name_plural = 'Группы Telegram страниц'

    def __str__(self):
        return f'{self.name}-{self.user}'


class TelegramSubscribePage(models.Model):
    def get_page_photo_path(self, filename: str) -> str:
        return f'subscribe_page/{self.instagram_username}/page_photos/{filename}'

    def get_instagram_avatar_path(self, filename: str) -> str:
        return f'subscribe_page/{self.instagram_username}/instagram_avatars/{filename}'

    @classmethod
    def slug_generate(cls, user: settings.AUTH_USER_MODEL, count: int = 1):
        slug = f'{user.username}-{cls.objects.filter(user=user).count() + count}'.replace(
            '.', '_')
        if cls.objects.filter(slug=slug):
            return cls.slug_generate(user, count + 1)
        return slug

    tg_bot_url = models.URLField(max_length=200)
    tg_channel_id = models.CharField(max_length=200)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='tg_subscribe_pages',
        verbose_name=_('Пользователь')
    )
    group = models.ForeignKey(
        TelegramGroupOfSubscribePage, on_delete=models.SET_NULL,
        related_name='tg_subscribe_pages',
        null=True, blank=True,
        verbose_name=_('Группа страниц')
    )
    domain = models.ForeignKey(
        Domain, on_delete=models.SET_NULL,
        related_name='tg_subscribe_pages',
        blank=True, null=True,
        verbose_name=_('Домен')
    )
    page_name = models.CharField(
        max_length=60,
        verbose_name=_('Название страницы')
    )
    slug = models.SlugField(
        max_length=30, db_index=True, unique=True,
        verbose_name=_('Ссылка подписной страницы')
    )
    page_photo = models.ImageField(
        upload_to=get_page_photo_path,
        blank=True, null=True,
        verbose_name=_('Page photo')
    )
    bg_color = models.ForeignKey(
        BGColor, related_name='tg_subscribe_pages',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Цвет фона')
    )

    title = models.CharField(
        max_length=60, null=True,
        verbose_name=_('Заголовок')
    )
    description = models.TextField(
        null=True,
        verbose_name=_('Описание')
    )
    button_text = models.CharField(
        max_length=30,
        default=_('ПОЛУЧИТЬ'),
        verbose_name=_('Текст на кнопке')
    )

    instagram_username = models.CharField(
        max_length=40, null=True,
        verbose_name=_('Ник в Instagram')
    )
    instagram_name = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name=_('Имя в Instagram')
    )
    instagram_avatar = models.ImageField(
        upload_to=get_instagram_avatar_path,
        blank=True, null=True,
        verbose_name=_('Аватарка Instagram')
    )

    timer_text = models.CharField(
        max_length=39, blank=True, null=True,
        default=_('Материал станет недоступным через:'),
        verbose_name=_('Текст на таймере')
    )
    is_timer_active = models.BooleanField(
        default=False,
        verbose_name=_('Таймер обратного отсчёта')
    )
    timer_time = models.IntegerField(
        default=180,
        verbose_name=_('Время таймера (в секундах)')
    )

    facebook_pixel = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('Facebook пиксель')
    )
    tiktok_pixel = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('Tiktok пиксель')
    )
    vk_pixel = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('ВК пиксель')
    )
    yandex_pixel = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('Яндекс метрика')
    )
    roistat_id = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_('Roistat ID')
    )

    ctr = models.FloatField(
        default=0, blank=True, null=True,
        verbose_name=_('CTR')
    )

    popup_title = models.CharField(
        max_length=50,
        default=_('Успешно'),
        verbose_name=_('Заголовок')
    )
    popup_text = models.TextField(
        default=_('Можете получить материалы, нажав по кнопке ниже.'),
        verbose_name=_('Текст'))
    popup_button_url = models.TextField(
        null=True,
        verbose_name=_('Ссылка кнопки')
    )
    popup_button_text = models.CharField(
        max_length=19,
        default=_('ПОЛУЧИТЬ МАТЕРИАЛЫ'),
        verbose_name=_('Текст на кнопке')
    )

    # Расширенные настройки
    presubscribe_text = models.CharField(
        max_length=255,
        default=_(
            'Подпишись на мой инстаграм и '
            'ссылка для скачивания материалов станет доступна'
        ),
        verbose_name=_('Текст перед подпиской')
    )
    precheck_subscribe_text = models.CharField(
        max_length=255,
        default=_('Введите ваш логин инстаграма для проверки подписки'),
        verbose_name=_(
            'Текст "Введите ваш логин инстаграма для проверки подписки"')
    )

    enter_login_placeholder = models.CharField(
        max_length=255,
        default=_('введите ваш логин'),
        verbose_name=_('Текст "Введите ваш логин"')
    )
    help_text = models.CharField(
        max_length=255,
        default=_('Здесь находится логин'),
        verbose_name=_('Текст "Здесь находиться логин" (подсказка)')
    )

    subscribe_button = models.CharField(
        max_length=255,
        default=_('Подписаться'),
        verbose_name=_('Текст "Подписаться" на кнопке')
    )
    already_subscribed_text = models.CharField(
        max_length=255,
        default=_('Я уже подписался'),
        verbose_name=_('Текст "Я уже подписался" под кнопкой')
    )

    subscribed_button = models.CharField(
        max_length=255,
        default=_('Подписался'),
        verbose_name=_('Текст "Я подписался" на кнопке')
    )
    not_yet_subscribed = models.CharField(
        max_length=255,
        default=_('Я еще не подписался'),
        verbose_name=_('Текст "Я еще не подписался" под кнопкой')
    )

    presearch_text = models.CharField(
        max_length=255,
        default=_('После подписки вернись на эту страницу для подтверждения'),
        verbose_name=_(
            'Текст "После подписки вернись на эту страницу для подтверждения"'
        )
    )
    search_text = models.CharField(
        max_length=255,
        default=_('Поиск аккаунта...'),
        verbose_name=_('Текст "Поиск аккаунта..."')
    )
    search_time_text = models.CharField(
        max_length=255,
        default=_('Это может занять до 20 секунд'),
        verbose_name=_('Текст "Это может занять до 20 секунд"')
    )
    success_text = models.CharField(
        max_length=255,
        default=_('Аккаунт найден!'),
        verbose_name=_('Текст "Аккаунт найден"')
    )
    error_text = models.CharField(
        max_length=255,
        default=_('Аккаунт не найден!'),
        verbose_name=_('Текст "Аккаунт не найден"')
    )

    single_page = models.BooleanField(default=False)
    show_subscribers = models.BooleanField(default=False)

    following_count = models.CharField(max_length=12, blank=True, null=True)
    follower_count = models.CharField(max_length=12, blank=True, null=True)
    media_count = models.CharField(max_length=12, blank=True, null=True)

    is_active = models.BooleanField(default=False, verbose_name=_('Активный'))
    created = models.BooleanField(default=False, verbose_name=_('Создано'))

    class Meta:
        verbose_name = 'Подписная страница'
        verbose_name_plural = 'Подписные страницы'

    def get_absolute_url(self) -> str:
        return reverse_lazy('subscribe_pages:page-detail', args=(self.slug,))

    def get_page_photo_url(self) -> str:
        if self.page_photo:
            return f'{settings.DOMAIN}{self.page_photo.url}' 
        return '#'

    def set_default_group(self):
        default_group, default_group_created = \
            GroupOfSubscribePage.objects.get_or_create(
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
        return f'{self.page_domain}/page/{self.slug}'

    @property
    def page_domain(self) -> str:
        if self.domain:
            domain = self.domain.domain
        else:
            domain = settings.DOMAIN
        return domain

    def calculate_ctr(self) -> float:
        all_views, all_subscribers = \
            InstagramStatistic.get_all_views_and_subscribers(self)
        try:
            ctr = all_subscribers / all_views * 100
        except ZeroDivisionError:
            ctr = 0
        return ctr

    def save_ctr(self, ctr: Optional[float] = None) -> None:
        if not ctr:
            ctr = self.calculate_ctr()
        self.ctr = float('{:.2f}'.format(ctr))
        self.save(update_fields=['ctr'])

    def all_views_subscribers_and_ctr(self) -> List[int]:
        all_views, all_subscribers = InstagramStatistic.get_all_views_and_subscribers(
            self)
        return [all_views, all_subscribers, self.ctr]

    all_views_subscribers_and_ctr.short_description = '👁‍🗨, 👤, %'

    @staticmethod
    def deactivate_user_subscribe_pages(user: settings.AUTH_USER_MODEL):
        for subscribe_page in user.subscribe_pages.filter(is_active=True):
            subscribe_page.is_active = False
            subscribe_page.save(update_fields=['is_active'])

    @staticmethod
    def activate_user_subscribe_pages(user: settings.AUTH_USER_MODEL):
        for subscribe_page in user.subscribe_pages.filter(is_active=False):
            subscribe_page.is_active = True
            subscribe_page.save(update_fields=['is_active'])

    @classmethod
    def is_slug_unique(cls, slug) -> bool:
        return not cls.objects.filter(slug=slug)

    def __str__(self):
        return f'{self.page_name} - {self.slug}'


class TelegramSubscriber(models.Model):
    telegram_subscribe_page = models.ForeignKey(
        TelegramSubscribePage, on_delete=models.CASCADE)
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.telegram_subscribe_page.telegram_bot_url} <- {self.telegram_user.telegram_username}'


@receiver(post_save, sender=InstagramSubscribePage)
def subscribe_page_post_save(sender, created, instance: InstagramSubscribePage,
                             **kwargs):
    if created:

        InstagramStatistic.objects.create(
            subscribe_page=instance, day=datetime.today()
        )

        default_group = GroupOfSubscribePage.objects.get(
            user=instance.user, name='Неотсортированные'
        )
        instance.group = default_group

        instance.instagram_username = instance.instagram_username.lower()
        instance.slug = instance.slug.lower()
        instance.created = True

        if not instance.instagram_name:
            instance.instagram_name = instance.instagram_username
        instance.save(
            update_fields=[
                'instagram_username', 'slug', 'created',
                'instagram_name', 'instagram_avatar',
                'group'
            ]
        )

        # если баланс больше 0, то подписная страница становится активной
        if instance.user.pocket.balance > 0:
            instance.is_active = True
            instance.save(update_fields=['is_active'])


@receiver(post_save, sender=VKSubscribePage)
def vk_subscribe_page_post_save(sender, created, instance: VKSubscribePage,
                                **kwargs):
    #    ipLogger.warning('signal ', end='')
    if created:
        #        ipLogger.warning('started: ')
        VKStatistic.objects.create(
            vk_subscribe_page=instance, day=datetime.today()
        )
        #        ipLogger.warning('123')
        default_group, default_group_created = VKGroupOfSubscribePage.objects.get_or_create(
            user=instance.user, name='Неотсортированные'
        )
        instance.group = default_group

        instance.slug = instance.slug.lower()
        instance.created = True

        instance.save(
            update_fields=[
                'slug', 'created',
                'group'
            ]
        )
        #        ipLogger.warning('jopa')
        # если баланс больше 0, то подписная страница становится активной
        if instance.user.pocket.balance > 0:
            instance.is_active = True
            instance.save(update_fields=['is_active'])
