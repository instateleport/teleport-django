# Generated by Django 3.0.5 on 2022-11-11 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0083_auto_20221111_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramsubscribepage',
            name='popup_button_url',
        ),
        migrations.RemoveField(
            model_name='telegramsubscribepage',
            name='popup_text',
        ),
    ]
