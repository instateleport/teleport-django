# Generated by Django 3.0.5 on 2022-03-29 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0054_vksubscriber_vksubscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vksubscriber',
            name='vk_user_id',
            field=models.BigIntegerField(unique=True, verbose_name='ID пользователя ВК'),
        ),
    ]