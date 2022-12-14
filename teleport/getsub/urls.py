from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

# local imports
from .robots import robots_txt
from .sitemaps import MounthlyChangefreqStaticViewSitemap


sitemaps = {
    'static': MounthlyChangefreqStaticViewSitemap,
}

urlpatterns = [
    path('api/v1/auth/', include('rest_framework.urls',
                                 namespace='rest_framework')),

    path('1/2/3/admin/', admin.site.urls),
    path('admin/clearcache/', include('clearcache.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.payment.urls')),
    path('', include('apps.partners.urls')),
    path('', include('apps.subscribe_pages.urls')),
    path('', include('apps.tg_subscribe_pages.urls')),
    path('', include('apps.stats.urls')),
    path('api/v1/', include('apps.api.urls')),
    path('robots.txt/', robots_txt, name='robots_txt'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    if settings.STATIC_ROOT:
        urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)