from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html

from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'user_change',
        'order_sum', 'paid',
        'created'
    ]
    list_per_page = 10

    search_fields = ['user__username']

    readonly_fields = ['created']

    def user_change(self, obj):
        url = reverse_lazy("admin:users_customuser_change", args=(obj.user.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    user_change.short_description = ''


@admin.register(models.OrderCent)
class OrderCentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'user_change',
        'order_sum', 'paid',
        'created'
    ]
    list_per_page = 10

    search_fields = ['user__username']

    readonly_fields = ['created']

    def user_change(self, obj):
        url = reverse_lazy("admin:users_customuser_change", args=(obj.user.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    user_change.short_description = ''
