from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings

from . import views


urlpatterns = [
    path('link-subscribe-telegram-page/', views.LinkTelegramAccountAPIView.as_view()),
    path('update-subscribe-telegram-page-statistic/', views.UpdateTelegramPageSubscribesStatiscticAPIView.as_view()),
    path('get-instagram-profile-data/', cache_page(settings.CACHE_TTL * 3)(views.GetInstagramProfileDataByUsername.as_view())),
]
