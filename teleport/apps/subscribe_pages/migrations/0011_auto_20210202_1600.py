# Generated by Django 3.0.5 on 2021-02-02 10:00

import apps.subscribe_pages.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscribe_pages', '0010_auto_20210118_1838'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='costpersubscriber',
            options={'verbose_name': 'Стоимость за одну подписку', 'verbose_name_plural': 'Стоимость за одну подписку'},
        ),
        migrations.AlterModelOptions(
            name='instagramcreator',
            options={'verbose_name': 'Instagram пользователя', 'verbose_name_plural': 'Instagram пользователей'},
        ),
        migrations.AlterModelOptions(
            name='instagramstatistic',
            options={'ordering': ('subscribe_page',), 'verbose_name': 'Статистика', 'verbose_name_plural': 'Статистики'},
        ),
        migrations.AlterModelOptions(
            name='instagramsubscribepage',
            options={'verbose_name': 'Подписная страница', 'verbose_name_plural': 'Подписные страницы'},
        ),
        migrations.AlterModelOptions(
            name='instagramsubscriber',
            options={'verbose_name': 'Подписчик', 'verbose_name_plural': 'Подписчики'},
        ),
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='presubscribe_text',
            field=models.CharField(default='Подпишись на мой инстаграм и ссылка для скачивания материалов станет доступна', max_length=255, verbose_name='Текст перед подпиской'),
        ),
        migrations.AlterField(
            model_name='costpersubscriber',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='button_text',
            field=models.CharField(default='ПОЛУЧИТЬ', max_length=30, verbose_name='Текст на кнопке'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='ctr',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='CTR'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='description',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='facebook_pixel',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Facebook пиксель'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='instagram_avatar',
            field=models.ImageField(blank=True, null=True, upload_to=apps.subscribe_pages.models.InstagramSubscribePage.get_instagram_avatar_path, verbose_name='Аватарка Instagram'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='instagram_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя в Instagram'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='instagram_username',
            field=models.CharField(max_length=40, null=True, verbose_name='Ник в Instagram'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='is_timer_active',
            field=models.BooleanField(default=False, verbose_name='Таймер обратного отсчёта'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='page_name',
            field=models.CharField(max_length=60, verbose_name='Название страницы'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='popup_button_url',
            field=models.CharField(max_length=255, null=True, verbose_name='Ссылка кнопки'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='popup_text',
            field=models.TextField(default='Можете получить материал, нажав по кнопке ниже.', verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='popup_title',
            field=models.CharField(default='Успешно', max_length=50, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='slug',
            field=models.SlugField(max_length=30, unique=True, verbose_name='Ссылка страницы'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='timer_text',
            field=models.CharField(blank=True, default='Материал станет недоступным через:', max_length=39, null=True, verbose_name='Текст на таймере'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='timer_time',
            field=models.IntegerField(default=180, verbose_name='Время таймера (в секундах)'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='title',
            field=models.CharField(max_length=60, null=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe_pages', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='instagramsubscriber',
            name='instagram_username',
            field=models.CharField(max_length=50, verbose_name='Ник в Instagram'),
        ),
        migrations.AlterField(
            model_name='instagramsubscriber',
            name='subscribe_to',
            field=models.ManyToManyField(related_name='subscribers', to='subscribe_pages.InstagramSubscribePage', verbose_name='Подписки'),
        ),
        migrations.AlterField(
            model_name='instagramsubscriber',
            name='views',
            field=models.ManyToManyField(related_name='views', to='subscribe_pages.InstagramSubscribePage', verbose_name='Просмотры'),
        ),
    ]
