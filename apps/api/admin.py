from django.contrib import admin

from .models import TelegramUser, TelegramChannel


admin.site.register(TelegramUser)
admin.site.register(TelegramChannel)