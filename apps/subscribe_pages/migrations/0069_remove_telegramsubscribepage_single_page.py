# Generated by Django 3.0.5 on 2022-11-10 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0068_auto_20221109_1839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramsubscribepage',
            name='single_page',
        ),
    ]