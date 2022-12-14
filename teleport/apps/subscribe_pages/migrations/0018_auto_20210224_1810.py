# Generated by Django 3.0.5 on 2021-02-24 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0017_instagramsubscribepage_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='popup_button_text',
            field=models.CharField(default='ПОЛУЧИТЬ МАТЕРИАЛЫ', max_length=19, verbose_name='Текст на кнопке'),
        ),
        migrations.AlterField(
            model_name='instagramsubscribepage',
            name='popup_text',
            field=models.TextField(default='Можете получить материалы, нажав по кнопке ниже.', verbose_name='Текст'),
        ),
    ]
