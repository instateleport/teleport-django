# Generated by Django 3.0.5 on 2022-12-04 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0097_auto_20221129_1745'),
        ('api', '0009_auto_20221202_1843'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TelegramUser',
            new_name='TelegramBotUser',
        ),
        migrations.DeleteModel(
            name='TelegramChannel',
        ),
    ]