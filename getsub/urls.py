from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

# local imports
from apps.users.views import handler404, handler500

from .robots import robots_txt

urlpatterns = [
    path('api/v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

    path('api/v1/auth/', include('rest_framework.urls',
                                 namespace='rest_framework')),

    path('1/2/3/admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('', include('apps.payment.urls')),
    path('', include('apps.partners.urls')),
    path('', include('apps.subscribe_pages.urls')),
    path('robots.txt/', robots_txt, name='robots_txt')
]

if settings.DEBUG:
    if settings.STATIC_ROOT:
        urlpatterns += static(settings.STATIC_URL,
                              document_root=settings.STATIC_ROOT)
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)

handler404 = handler404
handler500 = handler500
