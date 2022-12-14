# Generated by Django 3.0.5 on 2021-03-18 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0008_auto_20210318_2334'),
        ('users', '0005_customuser_is_referral'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='referrer_channel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='partners.Channel', verbose_name='Канал пригласителя'),
        ),
    ]
