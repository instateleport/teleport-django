from rest_framework import serializers


class LinkTelegramAccount(serializers.Serializer):
    telegram_username = serializers.CharField(max_length=200)
    page_hash = serializers.CharField(max_length=200)
    telegram_bot_url = serializers.CharField(max_length=200)


class NewTelegramChannelSubscriberSerializer(serializers.Serializer):
    page_hash = serializers.CharField(max_length=200)
    chat_id = serializers.IntegerField()
    channel_id = serializers.IntegerField()
    username = serializers.CharField(max_length=200)


class GetInstagramProfileDataByUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)