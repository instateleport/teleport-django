# Generated by Django 3.0.5 on 2021-02-18 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_pages', '0013_domain'),
    ]

    operations = [
        migrations.CreateModel(
            name='ISPManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, verbose_name='Имя пользователя')),
                ('password', models.CharField(max_length=255, verbose_name='Пароль')),
                ('auth_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='AUTH ID')),
                ('url', models.TextField(verbose_name='Ссылка ISPManager')),
            ],
        ),
    ]
