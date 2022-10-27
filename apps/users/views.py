from django.views.generic import TemplateView, RedirectView, DetailView, ListView, View
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.views import LoginView, FormView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, Http404, HttpResponse

# local imports
from apps.partners.models import Partner, Channel

from apps.payment.models import Order, OrderCent
from apps.payment.forms import PaymentForm
from apps.payment.unitpay_api import create_payment_url

from .mixins import (
    RedirectAuthenticatedUserMixin, IsResetPasswordMixin,
    IsNotResetPasswordMixin, IsAdminMixin
)
from . import models
from . import forms
from . import task

import logging


logger = logging.getLogger('register')


class HeadTemplateView(TemplateView):
    template_name = 'head-page.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            referral_url = request.GET.get('r')
            try:
                channel = Channel.objects.get(url=referral_url)
                partner = channel.partner
                user_id = partner.referrer.id

                partner.clicks += 1
                channel.clicks += 1
                partner.save(update_fields=['clicks'])
                channel.save(update_fields=['clicks'])

                request.session['referrer'] = user_id
                request.session['channel_id'] = channel.id
            except Channel.DoesNotExist:
                pass
        return super().get(request, *args, **kwargs)


class PublicOfferTemplateView(TemplateView):
    template_name = 'public-offer.html'


class PrivacyPolicyTemplateView(TemplateView):
    template_name = 'privacy-policy.html'


class TutorialTemplateView(LoginRequiredMixin, IsResetPasswordMixin, TemplateView):
    template_name = 'users/tutorial.html'


class SignInView(LoginView):
    authentication_form = forms.CustomUserAuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('subscribe_pages:page-list')
    redirect_authenticated_user = reverse_lazy('subscribe_pages:page-list')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def render_to_response(self, context, **response_kwargs):
        # добавляем ошибку, если пользователь ввёл неправильные данные
        if self.request.method == 'POST':
            form = context['form']
            if not form.is_valid():
                context.update({'errors': form.errors.get('__all__')})

        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )


class RegisterView(RedirectAuthenticatedUserMixin, FormView):
    form_class = forms.CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('subscribe_pages:page-list')

    def post(self, request, *args, **kwargs):
        try:
            form = self.get_form()
            if form.is_valid():
                user = form.save()
                referrer = request.session.get('referrer')
                channel_id = request.session.get('channel_id')
                if referrer:
                    is_referral = True
                    try:
                        referrer = models.CustomUser.objects.get(id=referrer)
                        referrer.partner.referrals.add(user)
                    except models.CustomUser.DoesNotExist:
                        is_referral = False

                    try:
                        channel = Channel.objects.get(id=channel_id)
                        channel.registered.add(user)
                        user.referrer_channel = channel
                    except Channel.DoesNotExist:
                        pass

                    user.is_referral = is_referral
                    user.save(update_fields=['is_referral', 'referrer_channel'])
                login(request, user)
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        except Exception as e:
            logger.warning(f'{timezone.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}: register_error - {e}')
            return HttpResponse('', status=500)


class PasswordResetView(RedirectAuthenticatedUserMixin, FormView):
    success_url = reverse_lazy('users:head')
    form_class = forms.CustomPasswordResetForm
    template_name = 'users/reset_password.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            task.reset_password.delay((email,))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class VerifyView(RedirectAuthenticatedUserMixin, RedirectView):
    url = reverse_lazy('users:change-password')

    def get(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(models.CustomUser, verification_uuid=kwargs.get('uuid'))
        except ValidationError:
            raise Http404()
        user.is_change_password = True
        user.save(update_fields=['is_change_password'])
        login(request, user)

        return super().get(request, *args, **kwargs)


class CustomPasswordChangeView(IsNotResetPasswordMixin, PasswordChangeView):
    form_class = forms.CustomUserSetPasswordForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('subscribe_pages:page-list')

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            request.user.is_change_password = False
            request.user.save()
            update_session_auth_hash(request, form.user)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class BalanceFormView(LoginRequiredMixin, IsResetPasswordMixin, ListView, FormMixin):
    model = OrderCent
    paginate_by = 10
    context_object_name = 'orders'

    form_class = PaymentForm

    template_name = 'users/balance.html'
    success_url = reverse_lazy('users:balance')

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user).order_by('-created')
        return queryset

    # def get_context_data(self, **kwargs):
    #     orders = self.get_queryset()
    #     page = int(self.request.GET.get('page', 1))
    #     paginator = Paginator(orders, 1)
    #
    #     context = super().get_context_data(**kwargs)
    #     context['orders'] = paginator.get_page(page)
    #     context['pages'] = paginator.page_range
    #     context['current_page'] = page
    #     context['prev_page'] = page - 1 if (page - 1) in context['pages'] else page
    #     context['next_page'] = page + 1 if (page + 1) in context['pages'] else page
    #     return context

    def form_valid(self, form):
        order_sum = form.cleaned_data['order_sum']
        user = self.request.user

        referrer_id = 0
        referrer_earned = 0
        if user.is_referral:
            try:
                referrer = Partner.objects.get(referrals=user)
                referrer_earned = order_sum * referrer.percent / 100
                referrer_id = referrer.id
            except Partner.DoesNotExist:
                pass

        order = OrderCent.objects.create(
            user=user,
            order_sum=order_sum,
            bonus=30,
            description=f'{user.id}_{referrer_id}_{referrer_earned}',
        )
        response = create_payment_url(order)
        if response:
            order.cent_bill_id = response['bill_id']
            order.save(update_fields=['cent_bill_id'])

            self.success_url = response['link_page_url']
        else:
            self.success_url = ''
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object_list = self.get_queryset()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SettingsFormView(LoginRequiredMixin, IsResetPasswordMixin, FormView):
    template_name = 'users/settings.html'

    form_class = forms.CustomUserChangeForm

    second_form_class = forms.CustomUserPasswordChangeForm
    second_prefix = None
    second_initial = {}

    success_url = reverse_lazy('users:settings')

    def get_second_initial(self):
        return self.second_initial.copy()

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.prefix,
            'instance': self.request.user
        }

        # если меняется первая форма
        if self.request.method in ('POST', 'PUT') and 'user_change_form_name' in self.request.POST:
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES
            })
        return kwargs

    def get_second_form_kwargs(self):
        """Return the keyword arguments for instantiating the second_form."""
        kwargs = {
            'initial': self.get_second_initial(),
            'prefix': self.second_prefix,
            'user': self.request.user
        }

        # если меняется вторая форма
        if self.request.method in ('POST', 'PUT') and 'password_change_form_name' in self.request.POST:
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_second_form(self):
        return self.second_form_class(**self.get_second_form_kwargs())

    def get_context_data(self, **kwargs):
        """Insert the forms into the context dict."""
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        if 'second_form' not in kwargs:
            kwargs['second_form'] = self.get_second_form()
        return super().get_context_data(**kwargs)

    def second_form_valid(self, second_form):
        """If the second_form is valid, redirect to the supplied URL."""
        messages.success(self.request, 'Пароль успешно изменен')
        return HttpResponseRedirect(self.get_success_url())

    def second_form_invalid(self, second_form):
        """If the second_form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(second_form=second_form))

    def post(self, request, *args, **kwargs):
        if 'user_change_form_name' in request.POST:
            form = self.get_form()
            if form.is_valid():
                f = form.save(commit=False)
                f.email = f.email.lower()
                f.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif 'password_change_form_name' in request.POST:
            second_form = self.get_second_form()
            if second_form.is_valid():
                second_form.save()
                update_session_auth_hash(request, request.user)
                return self.second_form_valid(second_form)
            else:
                return self.second_form_invalid(second_form)
        return self.get(request, *args, **kwargs)


def handler404(request, exception):
    return render(request, 'exceptions/404.html', status=404)


def handler500(request, exception=None):
    return render(request, 'exceptions/500.html', status=500)


class ChangeThemeView(LoginRequiredMixin, View):

    def get(self, request):
        data = request.GET
        if data.get('white'):
            request.user.theme = 'white'
        else:
            request.user.theme = 'dark'
        request.user.save(update_fields=['theme'])
        return HttpResponse({'status': 'SUCCESS'})
