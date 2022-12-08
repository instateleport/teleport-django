# Generated by Django 3.0.5 on 2020-12-03 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscribe_pages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe_pages', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='instagramstatistic',
            name='subscribe_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistic', to='subscribe_pages.InstagramSubscribePage', verbose_name='Statistic'),
        ),
        migrations.AddField(
            model_name='instagramcreator',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instagrams', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]