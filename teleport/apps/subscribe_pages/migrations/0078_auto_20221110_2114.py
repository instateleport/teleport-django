# Generated by Django 3.0.5 on 2022-11-10 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0077_remove_telegramsubscribepage_button_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='telegramsubscribepage',
            options={'verbose_name': 'Подписная Telegram страница', 'verbose_name_plural': 'Подписные Telegram страницы'},
        ),
    ]
