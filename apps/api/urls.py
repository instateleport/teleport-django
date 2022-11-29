from django.urls import path

from . import views


urlpatterns = [
    path('link-telegram/', views.LinkTelegramAccountAPIView.as_view()),
]
