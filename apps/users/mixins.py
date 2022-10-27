from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.paginator import Paginator

import hashlib
import hmac


class IsResetPasswordMixin:
    redirect_url = reverse_lazy('users:change-password')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_change_password:
            return HttpResponseRedirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class IsNotResetPasswordMixin:
    redirect_url = reverse_lazy('subscribe_pages:page-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_change_password:
            return HttpResponseRedirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class RedirectAuthenticatedUserMixin:
    redirect_url = reverse_lazy('subscribe_pages:page-list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return HttpResponseRedirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class IsAdminMixin:
    redirect_url = reverse_lazy('users:head')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)
