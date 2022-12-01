from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import LinkTelegramAccount
from apps.subscribe_pages.models import TelegramSubscribePage


class LinkTelegramAccountAPIView(APIView):
    def put(self, request):
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

