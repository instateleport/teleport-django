# Generated by Django 3.0.5 on 2021-02-23 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0016_remove_domain_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramsubscribepage',
            name='domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscribe_pages', to='subscribe_pages.Domain', verbose_name='Домен'),
        ),
    ]
