from django.db.models import Q
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.http import HttpResponse

import os

import pandas as pd

from uuid import uuid4

import mimetypes

# local imports
from . import models


class PocketInline(admin.StackedInline):
    model = models.Pocket


@admin.register(models.CustomUser)
class CustomUserAdmin(ModelAdmin):
    readonly_fields = ['referrer_channel']

    exclude = [
        'first_name', 'last_name', 'avatar',
        'date_joined',
        'password'
    ]

    list_display = [
        'username', 'email',
        'pocket', 'pocket_change',
        'phone',
        'is_referral', 'referrer_change', 'referrer_user_change'
    ]
    list_per_page = 10

    search_fields = ['username', 'email']

    inlines = [PocketInline]

    actions = ['active_users_count', 'download_orders', 'download_not_active_users']

    def active_users_count(self, request, queryset):
        self.message_user(request, f'{queryset.filter(order__paid=True).count()} активных пользователей')
    active_users_count.short_description = 'Кол-во активных пользователей'

    def download_orders(self, request, queryset):
        orders = {
            'user': [],
            'email': [],
#            'order_amount': [],
#            'order_created': [],
            'phone': []
        }
        for user in queryset:
            orders['user'].append(user.username)
            orders['email'].append(user.email)
#            orders['order_amount'].append(order.order_sum)
#            orders['order_created'].append(f'{order.created.date()}')
            orders['phone'].append(user.phone)
        excel_file_path = f'media/excels/{request.user.id}'
        if not os.path.exists(excel_file_path):
            os.makedirs(excel_file_path, exist_ok=True)
        excel_file_name = excel_file_path + f'{uuid4()}.xlsx'

        df = pd.DataFrame(orders)
        df.to_excel(excel_file_name,)

        with open(excel_file_name, 'rb') as f:
            response = HttpResponse(f.read())

        file_type = mimetypes.guess_type(excel_file_name) or 'application/octet-stream'
        response['Content-Type'] = file_type
        response['Content-Length'] = str(os.stat(excel_file_name).st_size)
        response['Content-Disposition'] = "attachment; filename=orders.xlsx"
        os.remove(excel_file_name)
        return response
    download_orders.short_description = 'Скачать заказы'

    def download_not_active_users(self, request, queryset):
        users = {
            'Неактивные':
                {
                    'user': [],
                    'email': [],
                },
            'Более активные':
                {
                    'user': [],
                    'email': [],
                    'paid_count': [],
                    'paid_sum': [],
                    'last_pay': []
                }
        }
        for user in queryset:
            orders = user.orders.filter(paid=True)

            if orders.count() == 0:
                users['Неактивные']['user'].append(user.username)
                users['Неактивные']['email'].append(user.email)
            elif 1 <= orders.count() <= 5:
                paid_sum = 0
                last_pay = ''

                users['Более активные']['user'].append(user.username)
                users['Более активные']['email'].append(user.email)
                users['Более активные']['paid_count'].append(orders.count())
                for order in orders.order_by('id'):
                    paid_sum += order.order_sum
                    last_pay = order.created.date()
                users['Более активные']['paid_sum'].append(paid_sum)
                users['Более активные']['last_pay'].append(f'{last_pay}')

        excel_file_path = f'media/excels/{request.user.id}'
        if not os.path.exists(excel_file_path):
            os.makedirs(excel_file_path, exist_ok=True)
        excel_file_name = excel_file_path + f'{uuid4()}.xlsx'

        writer = pd.ExcelWriter(excel_file_name, 'xlsxwriter')

        df1 = pd.DataFrame(users['Неактивные'])
        df2 = pd.DataFrame(users['Более активные'])

        df1.to_excel(writer, sheet_name='Неактивные')
        df2.to_excel(writer, sheet_name='Более активные')

        writer.save()
        writer.close()

        with open(excel_file_name, 'rb') as f:
            response = HttpResponse(f.read())

        file_type = mimetypes.guess_type(excel_file_name) or 'application/octet-stream'
        response['Content-Type'] = file_type
        response['Content-Length'] = str(os.stat(excel_file_name).st_size)
        response['Content-Disposition'] = "attachment; filename=orders.xlsx"
        os.remove(excel_file_name)
        return response
    download_not_active_users.short_description = 'Скачать неактивных юзеров'

    def referrer_change(self, obj):
        if obj.referrer_channel:
            url = reverse_lazy("admin:users_customuser_change", args=(obj.referrer_channel.partner.referrer.id,))
            return format_html(
                '<a target="_blank" href="{}">{}</a>', url, obj.referrer_channel.partner.referrer.username)
        return format_html('')
    referrer_change.short_description = 'Пригласитель (польз.)'

    def referrer_user_change(self, obj):
        if obj.referrer_channel:
            url = reverse_lazy("admin:partners_partner_change", args=(obj.referrer_channel.partner.referrer.id,))
            return format_html(
                '<a target="_blank" href="{}">{}</a>', url, obj.referrer_channel.partner.referrer.username)
        return format_html('')
    referrer_user_change.short_description = 'Пригласитель (партн.)'

    def pocket_change(self, obj):
        url = reverse_lazy("admin:users_pocket_change", args=(obj.pocket.id,))
        return format_html(
            '<a target="_blank" href="{}">Изменить</a>', url)
    pocket_change.short_description = ''


@admin.register(models.Pocket)
class PocketAdmin(ModelAdmin):
    readonly_fields = ['user']
    list_display = [
        'user', 'user_change',
        'balance'
    ]
    list_per_page = 10

    search_fields = ['user__username']

    def user_change(self, obj):
        url = reverse_lazy("admin:users_customuser_change", args=(obj.user.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    user_change.short_description = '(польз.)'

    def user_change(self, obj):
        url = reverse_lazy("admin:payment_ordercent_changelist", args=(obj.user.id,))
        return format_html('<a target="_blank" href="{}">Заказы</a>', url)
    user_change.short_description = '(заказы.)'
