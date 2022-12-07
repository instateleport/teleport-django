# Generated by Django 3.0.5 on 2022-12-07 01:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0101_auto_20221205_2226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramstatistic',
            name='telegram_subscribe_page',
        ),
        migrations.RemoveField(
            model_name='telegramsubscribepage',
            name='bg_color',
        ),
        migrations.RemoveField(
            model_name='telegramsubscribepage',
            name='domain',
        ),
        migrations.RemoveField(
            model_name='telegramsubscribepage',
            name='group',
        ),
        migrations.RemoveField(
            model_name='telegramsubscribepage',
            name='telegram_user',
        ),
        migrations.RemoveField(
            model_name='telegramsubscribepage',
            name='user',
        ),
        migrations.RemoveField(
            model_name='telegramsubscriber',
            name='subscribe_to',
        ),
        migrations.RemoveField(
            model_name='telegramsubscriber',
            name='telegram_user',
        ),
        migrations.RemoveField(
            model_name='telegramsubscriber',
            name='views',
        ),
        migrations.RemoveField(
            model_name='telegramuser',
            name='subscribe_to',
        ),
        migrations.DeleteModel(
            name='TelegramGroupOfSubscribePage',
        ),
        migrations.DeleteModel(
            name='TelegramStatistic',
        ),
        migrations.DeleteModel(
            name='TelegramSubscribePage',
        ),
        migrations.DeleteModel(
            name='TelegramSubscriber',
        ),
        migrations.DeleteModel(
            name='TelegramUser',
        ),
    ]