# Generated by Django 3.0.5 on 2022-12-05 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0099_auto_20221205_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='telegram_chat_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
