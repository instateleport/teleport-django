# Generated by Django 3.0.5 on 2020-12-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.CharField(choices=[('man', 'man'), ('woman', 'woman')], default='man', max_length=10, verbose_name='Avatar'),
        ),
    ]