# Generated by Django 3.0.5 on 2021-04-14 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0030_auto_20210411_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='yandex_pixel',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Яндекс метрика'),
        ),
    ]
