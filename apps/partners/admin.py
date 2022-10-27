from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html


from .models import Partner, PartnerPocket, Channel, Payout


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    readonly_fields = ['earned', 'clicks']

    list_display = [
        'referrer', 'user_change',
        'percent',
        'earned', 'clicks', 'all_referrals_count'
    ]
    list_filter = ['percent']
    list_per_page = 10

    search_fields = ['referrer__username']

    def user_change(self, obj):
        url = reverse_lazy("admin:users_customuser_change", args=(obj.referrer.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    user_change.short_description = '(польз.)'


@admin.register(PartnerPocket)
class PartnerPocketAdmin(admin.ModelAdmin):
    readonly_fields = ['partner', 'reserved', 'pay_outed']

    list_display = [
        'partner', 'referrer_change', 'user_change',
        'balance', 'reserved', 'pay_outed'
    ]
    list_per_page = 10

    search_fields = ['partner__referrer__username']

    def referrer_change(self, obj):
        url = reverse_lazy("admin:partners_partner_change", args=(obj.partner.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    referrer_change.short_description = '(партн.)'

    def user_change(self, obj):
        url = reverse_lazy("admin:users_customuser_change", args=(obj.partner.referrer.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    user_change.short_description = '(польз.)'


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = [
        'partner', 'partner_change', 'user_change',
        'name', 'url',
        'earned', 'clicks', 'registered_count',
        'can_delete'
    ]
    list_filter = ['can_delete']
    list_per_page = 10

    search_fields = ['partner__referrer__username']

    def partner_change(self, obj):
        url = reverse_lazy("admin:partners_partner_change", args=(obj.partner.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    partner_change.short_description = '(партн.)'

    def user_change(self, obj):
        url = reverse_lazy("admin:users_customuser_change", args=(obj.partner.referrer.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    user_change.short_description = '(польз.)'


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = [
        'partner', 'partner_change', 'user_change',
        'amount', 'payment_type', 'payment_address',
        'is_pay_outed', 'created'
    ]
    list_filter = ['is_pay_outed', 'payment_type']
    list_editable = ['is_pay_outed']
    list_per_page = 10

    search_fields = ['partner__referrer__username']

    def partner_change(self, obj):
        url = reverse_lazy("admin:partners_partner_change", args=(obj.partner.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    partner_change.short_description = '(партн.)'

    def user_change(self, obj):
        url = reverse_lazy("admin:users_customuser_change", args=(obj.partner.referrer.id,))
        return format_html('<a target="_blank" href="{}">Изменить</a>', url)
    user_change.short_description = '(польз.)'
