from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.tg_subscribe_pages.models import TelegramSubscribePage
from apps.tg_subscribe_pages.models import TelegramUser

from apps.subscribe_pages.lamadava_api.lamadava import get_instagram_profile_data_by_username

from .serializers import LinkTelegramAccount
from .serializers import NewTelegramChannelSubscriberSerializer
from .serializers import GetInstagramProfileDataByUsernameSerializer
from .models import TelegramBotUser


class UpdateTelegramPageSubscribesStatiscticAPIView(APIView):
    def patch(self, request):
        serializer = NewTelegramChannelSubscriberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        page_hash = serializer.data['page_hash']
        chat_id = serializer.data['chat_id']
        username = serializer.data['username']

        telegram_subscribe_page_statistic = TelegramSubscribePage.objects.get(page_hash=page_hash).statistic.last()

        if not TelegramBotUser.objects.filter(chat_id=chat_id, telegram_subscribe_pages__page_hash=page_hash):
            TelegramBotUser.objects.get_or_create(chat_id=chat_id)
            TelegramUser.objects.get_or_create(
                username=username,
                chat_id=chat_id
            )
            TelegramSubscribePage.objects.get(
                page_hash=page_hash
            ).subscribed_tg_users.add(
                TelegramUser.objects.get(chat_id=chat_id)
            )

            TelegramBotUser.objects.get(chat_id=chat_id).telegram_subscribe_pages.add(
                TelegramSubscribePage.objects.get(page_hash=page_hash)
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
            print(telegram_subscribe_page.user.pocket.balance)
            telegram_subscribe_page.user.pocket.save()
            telegram_subscribe_page.save()

        return Response({
            'bot_button_text': telegram_subscribe_page.button_text,
            'bot_button_url': telegram_subscribe_page.button_url,
            'present_message': telegram_subscribe_page.message_after_getting_present,
            'presubscribe_message': telegram_subscribe_page.presubscribe_text
        })


class GetInstagramProfileDataByUsername(APIView):
    permission_classes = []

    def get(self, request):
        print(request.query_params)
        serializer = GetInstagramProfileDataByUsernameSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['username']

        return Response(get_instagram_profile_data_by_username(username))
