from django.urls import path

from . import views


urlpatterns = [
    path('link-subscribe-telegram-page/', views.LinkTelegramAccountAPIView.as_view()),
    path('update-subscribe-telegram-page-statistic/', views.UpdateTelegramPageSubscribesStatiscticAPIView.as_view()),
    path('get-instagram-profile-data/', views.GetInstagramProfileDataByUsername.as_view()),
]
