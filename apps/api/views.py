from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import LinkTelegramAccount, NewTelegramChannelSubscriberSerializer
from .models import TelegramUser, TelegramChannel
from apps.subscribe_pages.models import TelegramSubscribePage


class HandleNewTelegramChannelSubscriberAPIView(APIView):
    def patch(self, request):
        serializer = NewTelegramChannelSubscriberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        page_hash = serializer.data['page_hash']
        chat_id = serializer.data['chat_id']
        channel_id = serializer.data['channel_id']

        telegram_subscribe_page_statistic = TelegramSubscribePage.objects.get(page_hash=page_hash).statistic.first()

        if not TelegramUser.objects.filter(chat_id=chat_id):
            TelegramUser.objects.create(chat_id=chat_id)

        if not TelegramChannel.objects.filter(channel_id=channel_id):
            TelegramChannel.objects.create(
                channel_id=channel_id,
                telegram_user=TelegramUser.objects.get(chat_id=chat_id)
            )
            telegram_subscribe_page_statistic.subscribers += 1
            telegram_subscribe_page_statistic.save()

        return Response({
            'subscribers_count': telegram_subscribe_page_statistic.subscribers
        })



class LinkTelegramAccountAPIView(APIView):
    def patch(self, request):
        serializer = LinkTelegramAccount(data=request.data)
        serializer.is_valid(raise_exception=True)

        telegram_username = serializer.data['telegram_username']
        page_hash = serializer.data['page_hash']
        telegram_bot_url = serializer.data['telegram_bot_url']

        telegram_subscribe_page = TelegramSubscribePage.objects.get(page_hash=page_hash)
        telegram_subscribe_page.instagram_username = telegram_username
        telegram_subscribe_page.telegram_bot_url = telegram_bot_url
        telegram_subscribe_page.is_linked = True

        if telegram_subscribe_page.user.pocket.balance >= 1:
            telegram_subscribe_page.user.pocket.balance -= 1
        else:
            return Response({
                'error': 'На вашем счете недостаточно средств'
            })

        with transaction.atomic():
            telegram_subscribe_page.user.pocket.save()
            telegram_subscribe_page.save()

        return Response({
            'bot_button_text': telegram_subscribe_page.button_text,
            'bot_button_url': telegram_subscribe_page.button_url,
            'present_message': telegram_subscribe_page.message_after_getting_present,
            'presubscribe_message': telegram_subscribe_page.presubscribe_text
        })

