from django.db import models


class TelegramBotUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)