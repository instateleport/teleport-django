# Generated by Django 3.0.5 on 2021-02-21 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0014_ispmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='added',
            field=models.BooleanField(default=False, verbose_name='Добавлен'),
        ),
    ]
