from django.contrib import sitemaps
from django.urls import reverse_lazy


class MounthlyChangefreqStaticViewSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return [
            'users:head',
            'users:public-offer',
            'users:privacy-policy',
            'users:tutorial',
            'users:settings',
            'users:tutorial',
            'users:login',
            'users:register',
            'users:reset-password',
        ]

    def location(self, obj) -> str:
        return reverse_lazy(obj)
