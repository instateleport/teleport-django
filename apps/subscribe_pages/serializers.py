from rest_framework import serializers

# local imports
from .models import VKSubscribePage, VKStatistic, VKSubscriber, VKSubscription


class VKSubscribePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VKSubscribePage
        fields = [
            # general settings
            'id',
            'vk_group_id', 'type_group_id',
            'page_name', 'slug', 'page_photo',

            'bg_first_color', 'bg_second_color', 'text_color',
            'panel_bg_color', 'panel_text_color', 'panel_icon_color',

            'is_timer_active', 'timer_text', 'timer_time',

            # first page
            'title', 'description', 'button_text',

            # success page
            'success_title', 'success_text', 'success_button_text',
            'success_button_url'

        ]
        lookup_field = 'slug'


class VKSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VKSubscriber
        exclude = [
            'date'
        ]
        read_only_fields = ['id']


class VKSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VKSubscription
        fields = [
            'vk_subscriber', 'vk_page', 'subscribed', 'date'
        ]

    def update(self, instance: VKSubscription, validated_data):
        subscribed = validated_data.get('subscribed')
        instance.date = validated_data.get('date')
        if not instance.subscribed and subscribed:  # если еще не был подписан
            instance.subscribed = subscribed
            instance.pay_per_subscriber()
        instance.save(update_fields=['subscribed', 'date'])
        return instance


class TelegramSubscriberSerializer(serializers.Serializer):
    telegram_user_id = serializers.CharField(max_length=200)
    telegram_user_username = serializers.CharField(max_length=200)
    telegram_channel_id = serializers.CharField(max_length=200)
    telegram_subscribe_page_button_url = serializers.URLField(max_length=200)
