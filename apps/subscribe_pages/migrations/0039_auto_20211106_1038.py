# Generated by Django 3.0.5 on 2021-11-06 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0038_auto_20211103_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='help_text',
            field=models.CharField(default='Здесь находится логин', max_length=255, verbose_name='Текст "Здесь находиться логин" (подсказка)'),
        ),
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='presearch_text',
            field=models.CharField(default='После подписки вернись на эту страницу для подтверждения', max_length=255, verbose_name='Текст "После подписки вернись на эту страницу для подтверждения"'),
        ),
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='search_time_text',
            field=models.CharField(default='Это может занять до 20 секунд', max_length=255, verbose_name='Текст "Это может занять до 20 секунд"'),
        ),
    ]
