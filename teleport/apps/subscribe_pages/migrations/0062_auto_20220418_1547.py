# Generated by Django 3.0.5 on 2022-04-18 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0061_vksubscribepage_type_group_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vksubscription',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='Дата подписки'),
        ),
    ]