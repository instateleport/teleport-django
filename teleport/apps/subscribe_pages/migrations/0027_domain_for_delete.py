# Generated by Django 3.0.5 on 2021-04-07 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0026_bgcolor_text_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='for_delete',
            field=models.BooleanField(default=False),
        ),
    ]