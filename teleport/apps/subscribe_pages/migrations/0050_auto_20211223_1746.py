# Generated by Django 3.0.5 on 2021-12-23 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0049_auto_20211222_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='follower_count',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='following_count',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='media_count',
            field=models.CharField(max_length=12, null=True),
        ),
    ]