# Generated by Django 3.0.5 on 2021-12-28 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Телефон'),
        ),
    ]
