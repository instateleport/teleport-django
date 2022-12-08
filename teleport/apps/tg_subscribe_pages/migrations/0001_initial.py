# Generated by Django 3.0.5 on 2022-12-07 01:54

import apps.tg_subscribe_pages.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscribe_pages', '0102_auto_20221207_0154'),
        ('api', '0010_auto_20221204_1744'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramGroupOfSubscribePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('can_delete', models.BooleanField(default=True, verbose_name='Можно удалить')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tg_group_of_pages', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Группа Telegram страницы',
                'verbose_name_plural': 'Группы Telegram страниц',
            },
        ),
        migrations.CreateModel(
            name='TelegramSubscribePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_name', models.CharField(max_length=60, verbose_name='Название страницы')),
                ('slug', models.SlugField(max_length=30, unique=True, verbose_name='Ссылка подписной страницы')),
                ('title', models.CharField(blank=True, max_length=60, null=True, verbose_name='Заголовок')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('timer_text', models.CharField(blank=True, default='Материал станет недоступным через:', max_length=39, null=True, verbose_name='Текст на таймере')),
                ('is_timer_active', models.BooleanField(default=False, verbose_name='Таймер обратного отсчёта')),
                ('timer_time', models.IntegerField(default=180, verbose_name='Время таймера (в секундах)')),
                ('facebook_pixel', models.CharField(blank=True, max_length=255, null=True, verbose_name='Facebook пиксель')),
                ('tiktok_pixel', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tiktok пиксель')),
                ('vk_pixel', models.CharField(blank=True, max_length=255, null=True, verbose_name='ВК пиксель')),
                ('yandex_pixel', models.CharField(blank=True, max_length=255, null=True, verbose_name='Яндекс метрика')),
                ('roistat_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Roistat ID')),
                ('ctr', models.FloatField(blank=True, default=0, null=True, verbose_name='CTR')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активный')),
                ('created', models.BooleanField(default=False, verbose_name='Создано')),
                ('page_hash', models.CharField(max_length=200, unique=True)),
                ('telegram_bot_url', models.CharField(blank=True, max_length=200, null=True)),
                ('telegram_channel_id', models.CharField(blank=True, max_length=200, null=True)),
                ('message_after_getting_present', models.CharField(max_length=2000, verbose_name='Сообщение при выдаче подарка')),
                ('button_text', models.CharField(max_length=500, verbose_name='Текст на кнопке (бот)')),
                ('button_url', models.URLField(blank=True, null=True, verbose_name='Ссылка кнопки (бот)')),
                ('page_photo', models.ImageField(blank=True, null=True, upload_to=apps.tg_subscribe_pages.models.TelegramSubscribePage.get_page_photo_path, verbose_name='Page photo')),
                ('instagram_username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя в Telegram')),
                ('instagram_avatar', models.ImageField(blank=True, null=True, upload_to=apps.tg_subscribe_pages.models.TelegramSubscribePage.get_instagram_avatar_path, verbose_name='Аватарка Telegram')),
                ('popup_title', models.CharField(default='Успешно', max_length=50, verbose_name='Заголовок')),
                ('popup_button_text', models.CharField(default='ПОЛУЧИТЬ МАТЕРИАЛЫ', max_length=19, verbose_name='Текст на кнопке (подписная страница)')),
                ('presubscribe_text', models.CharField(default='Подпишись на мой телеграм и ссылка для скачивания материалов станет доступна', max_length=255, verbose_name='Текст перед подпиской')),
                ('show_subscribers', models.BooleanField(default=False)),
                ('following_count', models.CharField(blank=True, max_length=12, null=True)),
                ('follower_count', models.CharField(blank=True, max_length=12, null=True)),
                ('media_count', models.CharField(blank=True, max_length=12, null=True)),
                ('is_linked', models.BooleanField(default=False, verbose_name='Привязан')),
                ('bg_color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tg_subscribe_pages', to='subscribe_pages.BGColor', verbose_name='Цвет фона')),
                ('domain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tg_subscribe_pages', to='subscribe_pages.Domain', verbose_name='Домен')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tg_subscribe_pages', to='tg_subscribe_pages.TelegramGroupOfSubscribePage', verbose_name='Группа страниц')),
                ('telegram_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='telegram_subscribe_pages', to='api.TelegramBotUser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tg_subscribe_pages', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписная Telegram страница',
                'verbose_name_plural': 'Подписные Telegram страницы',
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('chat_id', models.CharField(max_length=100, unique=True)),
                ('subscribe_to', models.ManyToManyField(blank=True, related_name='subscribed_tg_users', to='tg_subscribe_pages.TelegramSubscribePage', verbose_name='Подписки')),
            ],
        ),
        migrations.CreateModel(
            name='TelegramSubscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=255, verbose_name='IP')),
                ('can_get_material', models.BooleanField(default=False, verbose_name='Может просматривать материал')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата')),
                ('subscribe_to', models.ManyToManyField(blank=True, related_name='subscribers', to='tg_subscribe_pages.TelegramSubscribePage', verbose_name='Подписки')),
                ('telegram_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tg_subscribe_pages.TelegramUser')),
                ('views', models.ManyToManyField(blank=True, related_name='views', to='tg_subscribe_pages.TelegramSubscribePage', verbose_name='Просмотры')),
            ],
            options={
                'verbose_name': 'Telegram Подписчик',
                'verbose_name_plural': 'Telegram Подписчики',
            },
        ),
        migrations.CreateModel(
            name='TelegramStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(verbose_name='Дата')),
                ('views', models.BigIntegerField(default=0, verbose_name='Просмотры')),
                ('subscribers', models.BigIntegerField(default=0, verbose_name='Подписки')),
                ('ctr', models.FloatField(blank=True, default=0, null=True, verbose_name='CTR')),
                ('telegram_subscribe_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistic', to='tg_subscribe_pages.TelegramSubscribePage', verbose_name='Страница Telegram')),
            ],
            options={
                'verbose_name': 'Статистика Telegram',
                'verbose_name_plural': 'Статистики Telegram',
                'ordering': ('telegram_subscribe_page',),
            },
        ),
    ]