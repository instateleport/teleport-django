# Generated by Django 3.0.5 on 2021-04-26 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0033_instagramsubscriber_can_get_material'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramsubscriber',
            name='instagram_username',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Ник в Instagram'),
        ),
        migrations.AlterField(
            model_name='instagramsubscriber',
            name='subscribe_to',
            field=models.ManyToManyField(blank=True, null=True, related_name='subscribers', to='subscribe_pages.InstagramSubscribePage', verbose_name='Подписки'),
        ),
        migrations.AlterField(
            model_name='instagramsubscriber',
            name='views',
            field=models.ManyToManyField(blank=True, null=True, related_name='views', to='subscribe_pages.InstagramSubscribePage', verbose_name='Просмотры'),
        ),
    ]
