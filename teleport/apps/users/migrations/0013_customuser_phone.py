# Generated by Django 3.0.5 on 2021-12-24 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_customuser_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=255, null=True, unique=True, verbose_name='Телефон'),
        ),
    ]
