# Generated by Django 3.0.5 on 2021-02-25 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0020_delete_ispmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='bgcolor',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активный'),
        ),
    ]
