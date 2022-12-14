# Generated by Django 3.0.5 on 2021-04-08 01:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0004_auto_20201206_1420'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='order',
            name='account',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='Идентификатор'),
        ),
        migrations.AlterField(
            model_name='order',
            name='bonus',
            field=models.IntegerField(default=0, verbose_name='Бонус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создано'),
        ),
        migrations.AlterField(
            model_name='order',
            name='description',
            field=models.CharField(max_length=150, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_currency',
            field=models.CharField(choices=[('RUB', 'RUB')], default='RUB', max_length=5, verbose_name='Курс платежа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_sum',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Оплачено'),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
