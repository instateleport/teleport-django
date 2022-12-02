from django.db import models


class TelegramUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)


class TelegramChannel(models.Model):
    channel_id = models.BigIntegerField(unique=True)
    telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='telegram_channels',
        null=True,
        blank=True
    )