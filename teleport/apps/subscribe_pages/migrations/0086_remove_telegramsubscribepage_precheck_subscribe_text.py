# Generated by Django 3.0.5 on 2022-11-11 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0085_auto_20221111_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramsubscribepage',
            name='precheck_subscribe_text',
        ),
    ]