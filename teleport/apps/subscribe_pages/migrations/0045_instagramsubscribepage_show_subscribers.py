# Generated by Django 3.0.5 on 2021-12-11 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0044_auto_20211129_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='show_subscribers',
            field=models.BooleanField(default=False),
        ),
    ]