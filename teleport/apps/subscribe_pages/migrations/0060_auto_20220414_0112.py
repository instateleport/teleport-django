# Generated by Django 3.0.5 on 2022-04-13 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0059_auto_20220409_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vksubscription',
            name='date',
            field=models.DateTimeField(verbose_name='Дата подписки'),
        ),
    ]