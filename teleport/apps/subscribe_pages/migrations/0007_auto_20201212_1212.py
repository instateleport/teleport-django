# Generated by Django 3.0.5 on 2020-12-12 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0006_auto_20201211_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='timer_text',
            field=models.CharField(blank=True, default='Материал станет недоступным через:', max_length=39, null=True, verbose_name='Timer text'),
        ),
    ]