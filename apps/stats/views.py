from datetime import date

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Count

from apps.users.mixins import IsAdminMixin

from apps.subscribe_pages.models import InstagramSubscriber, VKSubscription
from apps.users.models import CustomUser


class StatsView(LoginRequiredMixin, IsAdminMixin, View):
    template_name = 'stats.html'

    def get(self, request, *args, **kwargs):

        from datetime import timedelta

        cur_date = date.today()

        amount_of_system_users = CustomUser.objects.filter(
            date_joined__date=cur_date-timedelta(days=1)
        ).count()
        amount_of_instagram_subs = InstagramSubscriber.objects.filter(
            date__date=cur_date-timedelta(days=1)
        ).count()
        amount_of_vk_subs = VKSubscription.objects.filter(
            date__date=cur_date-timedelta(days=1)
        ).count()

        context = {
            'amount_of_system_users': amount_of_system_users,
            'amount_of_instagram_subs': amount_of_instagram_subs,
            'amount_of_vk_subs': amount_of_vk_subs
        }
        return render(request, self.template_name, context)