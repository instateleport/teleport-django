# Generated by Django 3.0.5 on 2022-11-09 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0067_auto_20221109_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramsubscribepage',
            name='tg_bot_url',
            field=models.URLField(default='https://t.me/open'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='telegramsubscribepage',
            name='tg_channel_id',
            field=models.CharField(default=-19869627198, max_length=200),
            preserve_default=False,
        ),
    ]