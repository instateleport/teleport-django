# Generated by Django 3.0.5 on 2021-04-23 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0032_instagramsubscribepage_vk_pixel'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsubscriber',
            name='can_get_material',
            field=models.BooleanField(default=False, verbose_name='Может просматривать материал'),
        ),
    ]