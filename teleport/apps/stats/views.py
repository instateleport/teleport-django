from datetime import date

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from apps.users.mixins import IsAdminMixin

from apps.subscribe_pages.models import InstagramSubscriber
from apps.subscribe_pages.models import VKSubscription
from apps.users.models import CustomUser
from apps.tg_subscribe_pages.models import TelegramSubscribePage


class StatsView(LoginRequiredMixin, IsAdminMixin, View):
    template_name = 'stats.html'

    def get(self, request, *args, **kwargs):

        from datetime import timedelta

        current_date = date.today()

        amount_of_system_users = CustomUser.objects.filter(
            date_joined__date=current_date - timedelta(days=1)
        ).count()
        amount_of_instagram_subs = InstagramSubscriber.objects.filter(
            date__date=current_date - timedelta(days=1)
        ).count()
        amount_of_vk_subs = VKSubscription.objects.filter(
            date__date=current_date - timedelta(days=1)
        ).count()
        amount_of_telegram_subs = TelegramSubscribePage.objects.filter(
            subscribed_tg_users__created_at=current_date - timedelta(days=1)
        ).count()

        context = {
            'amount_of_system_users': amount_of_system_users,
            'amount_of_instagram_subs': amount_of_instagram_subs,
            'amount_of_vk_subs': amount_of_vk_subs,
            'amount_of_telegram_subs': amount_of_telegram_subs,
        }
        return render(request, self.template_name, context)