from django.urls import path

from . import views


urlpatterns = [
    path('link-subscribe-telegram-page/', views.LinkTelegramAccountAPIView.as_view()),
    path('update-subscribe-telegram-page-statistic/', views.HandleNewTelegramChannelSubscriberAPIView.as_view())
]
