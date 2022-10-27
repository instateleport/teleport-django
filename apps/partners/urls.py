from django.urls import path

from . import views


app_name = 'partners'

urlpatterns = [
    path('partner/', views.PartnerDetailView.as_view(), name='cabinet'),

    path('partner/channel/create/', views.ChannelCreateView.as_view(), name='channel-create'),
    path('partner/channel/edit/', views.ChannelUpdateView.as_view(), name='channel-update'),
    path('partner/channel/delete/', views.ChannelDeleteView.as_view(), name='channel-delete'),

    path('partner/payout/create/', views.PayoutCreateView.as_view(), name='payout-create'),
]
