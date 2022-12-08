from django.apps import AppConfig


class PartnersConfig(AppConfig):
    name = 'apps.partners'
    verbose_name = 'Партнёрка'
    '''
    def ready(self):
        from .models import Partner, PartnerPocket, Channel

        from apps.users.models import CustomUser
        for user in CustomUser.objects.all():
            partner, partner_created = Partner.objects.get_or_create(referrer=user)
            PartnerPocket.objects.get_or_create(partner=partner)
            channels = Channel.objects.filter(partner=partner, name='Основной', can_delete=False)
            ch_count = len(channels)
            for i in channels:
                if ch_count == 1:
                    break
                else:
                    i.delete()
                    ch_count -= 1
            url = Channel.url_generate()
            channel, channel_created = Channel.objects.get_or_create(partner=partner, name='Основной',
                                                                     can_delete=False)

            channel.url = url
            channel.save(update_fields=['url'])
    '''
