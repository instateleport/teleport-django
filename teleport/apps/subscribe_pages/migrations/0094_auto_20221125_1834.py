# Generated by Django 3.0.5 on 2022-11-25 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0093_auto_20221125_1221'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupofsubscribepage',
            options={'verbose_name': 'Группа Instagram страниц', 'verbose_name_plural': 'Группы Instagram страниц'},
        ),
        migrations.AlterModelOptions(
            name='vkgroupofsubscribepage',
            options={'verbose_name': 'Группа VK страниц', 'verbose_name_plural': 'Группы VK страниц'},
        ),
    ]