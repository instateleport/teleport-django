# Generated by Django 3.0.5 on 2021-12-23 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0050_auto_20211223_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='follower_count',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='following_count',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='media_count',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]