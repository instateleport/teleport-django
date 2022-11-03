# Generated by Django 3.0.5 on 2022-11-03 10:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscribe_pages', '0063_merge_20220418_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramSubscribePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_bot_url', models.CharField(max_length=200)),
                ('telegram_channel_id', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='telegram_subscribe_pages', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_username', models.CharField(max_length=100)),
                ('telegram_user_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='vksubscription',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата подписки'),
        ),
        migrations.CreateModel(
            name='TelegramSubscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_subscribe_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscribe_pages.TelegramSubscribePage')),
                ('telegram_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscribe_pages.TelegramUser')),
            ],
        ),
    ]
