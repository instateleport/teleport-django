from django.contrib import admin

from . import models


@admin.register(models.TelegramGroupOfSubscribePage)
class TelegramGroupOfSubscribePageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'can_delete']
    search_fields = ['user__username', 'name']

@admin.register(models.TelegramSubscribePage)
class TelegramSubscribePageAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    pass


@admin.register(models.TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TelegramSubscriber)
class TelegramSubscriberAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TelegramStatistic)
class TelegramStatiscticAdmin(admin.ModelAdmin):
    pass