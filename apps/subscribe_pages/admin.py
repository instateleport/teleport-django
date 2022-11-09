from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html

# local imports
from . import models


@admin.register(models.BGColor)
class BGColorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.VKSubscribePage)
class VKSubscribePageAdmin(admin.ModelAdmin):
    list_display = [
        'page_name',
        'slug', 'user',
        'ctr', 'all_views_subscribers_and_ctr',
        'is_active'
    ]
    list_filter = ['user']
    list_per_page = 10


@admin.register(models.VKSubscriber)
class VKSubscriberAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'first_name', 'last_name', 'sex', 'country', 'date']
    list_filter = ['sex', 'country']

    search_fields = ['first_name', 'last_name', 'country']


@admin.register(models.VKSubscription)
class VKSubscriptionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['vk_subscriber', 'vk_page', 'subscribed', 'date']
    list_filter = ['subscribed', 'date']

    search_fields = ['vk_subscriber__first_name', 'vk_page__slug']


@admin.register(models.VKGroupOfSubscribePage)
class VKGroupOfSubscribePageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'can_delete']
    search_fields = ['user__username', 'name']


@admin.register(models.GroupOfSubscribePage)
class GroupOfSubscribePageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name']
    search_fields = ['user__username', 'name']


@admin.register(models.InstagramSubscribePage)
class SubscribePageAdmin(admin.ModelAdmin):
    list_display = [
        'page_name', 'page_statistics',
        'slug', 'page_open', 'pages_subscribers', 'pages_views',
        'user', 'user_change', 'user_page_list',
        'ctr', 'all_views_subscribers_and_ctr',
        'is_active'
    ]
    list_filter = ['user']
    list_per_page = 10

    search_fields = ['slug', 'user__username', 'instagram_username']

    def pages_subscribers(self, obj):
        url = reverse_lazy("admin:subscribe_pages_instagramsubscriber_changelist")
        return format_html('<a target="_blank" href="{}?subscribe_to__slug={}">см.</a>', url, obj.slug)
    pages_subscribers.short_description = 'подписчики'

    def pages_views(self, obj):
        url = reverse_lazy("admin:subscribe_pages_instagramsubscriber_changelist")
        return format_html('<a target="_blank" href="{}?views__slug={}">см.</a>', url, obj.slug)
    pages_views.short_description = 'просмотры'

    def user_change(self, obj):
        url = reverse_lazy("admin:users_customuser_change", args=(obj.user.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    user_change.short_description = ''

    def user_page_list(self, obj):
        url = reverse_lazy("admin:subscribe_pages_instagramsubscribepage_changelist")
        return format_html(
            '<a target="_blank" href="{}?user__id__exact={}">страницы пользователя</a>', url, obj.user.id)
    user_page_list.short_description = ''

    def page_open(self, obj):
        if obj.domain:
            url = f'https://{obj.domain.domain}/page/{obj.slug}'
        else:
            url = reverse_lazy("subscribe_pages:page-open", args=(obj.slug,))
        return format_html('<a target="_blank" href="{}">Открыть</a>', url)
    page_open.short_description = ''

    def page_statistics(self, obj):
        url = reverse_lazy("admin:subscribe_pages_instagramstatistic_changelist")
        return format_html('<a target="_blank" href="{}?subscribe_page__id__exact={}">Статистика</a>', url, obj.id)
    page_statistics.short_description = ''


@admin.register(models.InstagramStatistic)
class StatisticAdmin(admin.ModelAdmin):
    readonly_fields = ['subscribe_page', 'day', 'ctr', 'views', 'subscribers']

    list_display = [
        'subscribe_page', 'page_open', 'subscribe_page_link',
        'day', 'views', 'subscribers',
        'ctr', 'all_views_subscribers_and_ctr'
    ]
    list_filter = ['subscribe_page']
    list_per_page = 10

    search_fields = ['subscribe_page__page_name', 'subscribe_page__slug', 'subscribe_page__user__username']

    def page_open(self, obj):
        url = reverse_lazy("subscribe_pages:page-open", args=(obj.subscribe_page.slug,))
        return format_html('<a target="_blank" href="{}">Открыть страницу</a>', url)
    page_open.short_description = ''

    def subscribe_page_link(self, obj):
        url = reverse_lazy("admin:subscribe_pages_instagramsubscribepage_change", args=(obj.subscribe_page.id,))
        return format_html('<a target="_blank" href="{}">Изменить страницу</a>', url)
    subscribe_page_link.short_description = ''

    def all_views_subscribers_and_ctr(self, obj):
        return [obj.views, obj.subscribers, obj.ctr]
    all_views_subscribers_and_ctr.short_description = '👁‍🗨, 👤, %'


@admin.register(models.InstagramCreator)
class InstagramAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_change', 'instagram']
    list_per_page = 10

    search_fields = ['instagram']

    def user_change(self, obj):
        url = reverse_lazy("admin:users_customuser_change", args=(obj.user.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    user_change.short_description = ''


@admin.register(models.InstagramSubscriber)
class InstagramSubscriberAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['ip', 'instagram_username']
    list_filter = ['views__slug', 'subscribe_to__slug', 'views__statistic__day']

    search_fields = ['instagram_username', 'views__slug', 'subscribe_to__slug']


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
#    readonly_fields = ['user']
    list_display = ['domain', 'domain_open', 'user', 'user_change']
    list_per_page = 10

    search_fields = ['user__username', 'domain']

    exclude = ['for_delete']

    def domain_open(self, obj):
        url = 'https://{}'.format(obj.domain)
        return format_html('<a target="_blank" href="{}">Открыть</a>', url)
    domain_open.short_description = ''

    def user_change(self, obj):
        url = reverse_lazy("admin:users_customuser_change", args=(obj.user.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    user_change.short_description = ''


@admin.register(models.CostPerSubscriber)
class CostPerSubscriberAdmin(admin.ModelAdmin):
    pass

@admin.register(models.TelegramGroupOfSubscribePage)
class TelegramGroupOfSubscribePageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'can_delete']
    search_fields = ['user__username', 'name']

@admin.register(models.TelegramSubscribePage)
class TelegramSubscribePageAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    pass


@admin.register(models.TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TelegramSubscriber)
class TelegramSubscriberAdmin(admin.ModelAdmin):
    pass
