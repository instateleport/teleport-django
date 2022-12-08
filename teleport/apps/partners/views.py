from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from apps.users.mixins import IsResetPasswordMixin
from apps.subscribe_pages.mixins import AjaxMixin

from .mixins import IsChannelOwner
from . import models
from . import forms


class PartnerDetailView(LoginRequiredMixin, IsResetPasswordMixin, DetailView, FormMixin):
    model = models.Partner

    form_class = forms.ChannelCreateUpdateForm
    second_form_class = forms.PayoutCreateForm
    second_prefix = None
    second_initial = {}

    http_method_names = ['get']

    template_name = 'partners/partner.html'
    context_object_name = 'partner'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment_types'] = models.Payout.PAYMENT_CHOICES
        if 'second_form' not in context:
            context['second_form'] = self.get_second_form()
        return context

    def get_second_initial(self):
        return self.second_initial.copy()

    def get_second_form(self):
        return self.second_form_class(**self.get_second_form_kwargs())

    def get_second_form_kwargs(self):
        kwargs = {
            'initial': self.get_second_initial(),
            'prefix': self.second_prefix,
        }
        return kwargs

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, referrer=self.request.user)
        return obj


class ChannelCreateView(LoginRequiredMixin, IsResetPasswordMixin, CreateView, AjaxMixin):
    model = models.Channel
    form_class = forms.ChannelCreateUpdateForm

    success_url = reverse_lazy('partners:cabinet')

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.object = None
        response = self.get_ajax_response()
        form = self.get_form()

        if form.is_valid():
            f = form.save(commit=False)
            f.partner = request.user.partner
            f.url = models.Channel.url_generate()
            f.save()

            response['status'] = 'SUCCESS'
            response['data'] = {
                'channel_id': f.id,
                'name': f.name,
                'url': f.url
            }
        else:
            response['status'] = 'FAIL'
            response['reason'] = 'FORM_ERROR'
            response['errors'] = form.errors
        return self.ajax_response(response)


class ChannelUpdateView(LoginRequiredMixin, IsResetPasswordMixin, UpdateView, AjaxMixin):
    model = models.Channel
    form_class = forms.ChannelCreateUpdateForm

    success_url = reverse_lazy('partners:cabinet')

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        response = self.get_ajax_response()
        form = self.get_form()

        if form.is_valid():
            self.object = self.get_object()
            if self.object:
                self.object.name = form.cleaned_data['name']
                self.object.save(update_fields=['name'])
                response['status'] = 'SUCCESS'
                response['data'] = {
                    'channel_id': self.object.id,
                    'name': self.object.name
                }
            else:
                response['status'] = 'FAIL'
                response['reason'] = 'CHANNEL_NOT_FOUND'
        else:
            response['status'] = 'FAIL'
            response['reason'] = 'FORM_ERROR'
            response['errors'] = form.errors
        return self.ajax_response(response)

    def get_object(self, queryset=None):
        try:
            return self.get_queryset().get(pk=self.request.POST.get('channelId'))
        except self.model.DoesNotExist:
            return


class ChannelDeleteView(LoginRequiredMixin, IsResetPasswordMixin, DeleteView, AjaxMixin):
    model = models.Channel

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.object = None
        response = self.get_ajax_response()

        try:
            channel_id = int(request.POST.get('channelID'))
            self.object = self.model.objects.get(
                id=channel_id,
                partner=models.Partner.objects.get(referrer=request.user)
            )
            if self.object.can_delete:
                self.object.delete()
                response['status'] = 'SUCCESS'
                response['data'] = {
                    'channel_id': channel_id
                }
            else:
                response['status'] = 'FAIL'
                response['reason'] = 'CAN_NOT_DELETE'
        except (self.model.DoesNotExist, models.Partner.DoesNotExist):
            response['status'] = 'FAIL'
            response['reason'] = 'CHANNEL_NOT_FOUND'
        return self.ajax_response(response)


class PayoutCreateView(LoginRequiredMixin, IsResetPasswordMixin, CreateView, AjaxMixin):
    model = models.Payout
    form_class = forms.PayoutCreateForm

    success_url = reverse_lazy('partners:cabinet')

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        response = self.get_ajax_response()

        if form.is_valid(request.user.partner.pocket):
            f: models.Payout = form.save(commit=False)
            f.partner = request.user.partner
            f.save()

            response['status'] = 'SUCCESS'
            response['data'] = {
                'created_date': f'{f.created.date()}', 'created_time': f'{f.created.time().strftime("%H:%M")}',
                'amount': float(f.amount), 'payment_type': f.payment_type,
                'balance': f'{float(f.partner.pocket.balance):.2f}'.replace('.', ','),
                'payment_address': f.payment_address
            }
        else:
            response['status'] = 'FAIL'
            response['reason'] = 'FORM_ERROR'
            response['errors'] = form.errors
        return self.ajax_response(response)
