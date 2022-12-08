from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from . import views


app_name = 'users'

urlpatterns = [
    path('', views.HeadTemplateView.as_view(), name='head'),
    path('public-offer/', views.PublicOfferTemplateView.as_view(), name='public-offer'),
    path('privacy-policy/', views.PrivacyPolicyTemplateView.as_view(), name='privacy-policy'),

    path('tutorial/', views.TutorialTemplateView.as_view(), name='tutorial'),
    path('settings/', views.SettingsFormView.as_view(), name='settings'),
    path('balance/', views.BalanceFormView.as_view(), name='balance'),

    path('login/', views.SignInView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('reset/', views.PasswordResetView.as_view(), name='reset-password'),
    path('reset/<uuid>/', views.VerifyView.as_view(), name='verify'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change-password'),

    path('change-theme/', views.ChangeThemeView.as_view(), name='change-teme')
]

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
