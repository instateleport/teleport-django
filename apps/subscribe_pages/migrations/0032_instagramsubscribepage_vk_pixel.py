# Generated by Django 3.0.5 on 2021-04-22 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0031_auto_20210414_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='vk_pixel',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ВК пиксель'),
        ),
    ]
