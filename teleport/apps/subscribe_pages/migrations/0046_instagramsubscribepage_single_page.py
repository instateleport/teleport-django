# Generated by Django 3.0.5 on 2021-12-12 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0045_instagramsubscribepage_show_subscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='single_page',
            field=models.BooleanField(default=False),
        ),
    ]