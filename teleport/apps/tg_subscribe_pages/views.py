import os
import mimetypes
from uuid import uuid4
import logging

import pandas as pd
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import View
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import datetime
from django.utils import timezone
from celery.schedules import timedelta

from apps.users.mixins import IsResetPasswordMixin

from apps.subscribe_pages.mixins import IsSubscribePageActive
from apps.subscribe_pages.mixins import IsSubscribePageOwner
from apps.subscribe_pages.mixins import AjaxMixin
from apps.subscribe_pages.mixins import DeleteAjaxMixin
from apps.subscribe_pages.views import SubscribePageListMixin
from apps.subscribe_pages.models import BGColor
from apps.subscribe_pages.models import Domain

from .models import TelegramSubscribePage
from .models import TelegramGroupOfSubscribePage
from .models import TelegramStatistic
from .models import TelegramSubscriber

from . import forms


logger_page = logging.getLogger('page')


class TGSubscribePageOpenView(IsSubscribePageActive, DetailView):
    model = TelegramSubscribePage
    queryset = TelegramSubscribePage.objects.filter(created=True)
    template_name = 'subscribe_pages/tg-page-open.html'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bg_color'] = self.object.bg_color
        context['page_photo'] = self.object.get_page_photo_url()
        context['instagram_avatar'] = self.object.get_instagram_avatar_url()
        return context

    def get(self, request, *args, **kwargs):
        if not self.object:
            self.object = self.get_object()
        try:
            subscriber = TelegramSubscriber.get_or_create_by_user_ip(
                request)

            statistic, statistic_created = TelegramStatistic.objects.get_or_create(
                        telegram_subscribe_page=self.object, day=datetime.today())

            if not subscriber.is_visited_page_by_slug(self.object.slug):  # Если он не был на этой странице то
                try:
                    # получаем/создаём статистику сегодняшнего дня
                    statistic, statistic_created = TelegramStatistic.objects.get_or_create(
                        telegram_subscribe_page=self.object, day=datetime.today())

                except TelegramStatistic.MultipleObjectsReturned:
                    statistics = TelegramStatistic.objects.filter(
                        telegram_subscribe_page=self.object, day=datetime.today())
                    statistic = statistics[0]
                    for statistic_ in statistics[1:]:
                        statistic.views += statistic_.views
                        statistic_.delete()

                statistic.views += 1
                statistic.save(update_fields=['views'])
                subscriber.views.add(self.object)  # добавляем страницу в просмотренные
        except Exception as e:
            logger_page.warning(
                f'\n{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}: '
                f'error: {e}, '
                f'slug: {self.object.slug}, '
                f'ip: {request.META}')

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class TGSubscribePageDetailView(LoginRequiredMixin, IsResetPasswordMixin,
                              IsSubscribePageOwner, UpdateView):
    model = TelegramSubscribePage
    form_class = forms.TGSubscribePageUpdateForm
    template_name = 'subscribe_pages/tg-page-detail.html'
    success_url = reverse_lazy('tg-page-list')

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = self.model.objects.all()
        else:
            queryset = self.model.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not self.object:
            self.object = self.get_object()

        context['domain'] = self.object.domain
        context['domains'] = Domain.objects.filter(
            user=self.request.user)

        context['bg_color'] = self.object.bg_color
        context['bg_colors'] = BGColor.objects.filter(is_active=True)

        context['page_photo'] = f'https://{self.object.get_page_photo_url()}'
        context['instagram_avatar'] = self.object.get_instagram_avatar_url()
        context['instagram_username'] = self.object.instagram_username
        context['follower_count'] = 1000

        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class TGAddToFolderView(LoginRequiredMixin, AjaxMixin, View):
    def post(self, request, *args, **kwargs):
        response = self.get_ajax_response()
        data = request.POST
        page = TelegramSubscribePage.objects.get(
            slug=data['slug'], user=request.user
        )
        group = TelegramGroupOfSubscribePage.objects.get(
            user=request.user, id=int(data['group_id'])
        )
        page.group = group
        page.save()
        response['status'] = 'SUCCESS'
        response['url'] = '/tg-subscribe-pages/%s/' % group.name

        return self.ajax_response(response)


class TGSubscribePageDeleteView(LoginRequiredMixin, IsResetPasswordMixin,
                              DeleteAjaxMixin):
    model = TelegramSubscribePage
    id_field_name = 'pageID'
    is_owner = True


class TGFolderCreateView(LoginRequiredMixin, IsResetPasswordMixin, CreateView):
    model = TelegramGroupOfSubscribePage
    form_class = forms.TGGroupCreateForm
    template_name = 'subscribe_pages/tg-page-list.html'
    http_method_names = ['post']

    def get_success_url(self):
        return reverse_lazy('tg-page-list',
                            args=(self.object.name,))

    def form_invalid(self, form):
        messages.error(
            self.request, 'Название папки содержит запрещенные символы'
        )
        return HttpResponseRedirect(reverse_lazy('tg-page-list'))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            return self.form_valid(form)
        return self.form_invalid(form)


class TGFolderDeleteAjaxView(LoginRequiredMixin, IsResetPasswordMixin, DeleteAjaxMixin):
    model = TelegramGroupOfSubscribePage
    id_field_name = 'folderID'
    is_owner = True

    def delete(self, request, *args, **kwargs):
        response = self.get_ajax_response()
        data = request.POST
        object_id = int(data.get(self.id_field_name, 0))

        self.object = self.get_object(object_id)
        if self.object:
            for subscribe_page in self.object.tg_subscribe_pages.all():
                subscribe_page.set_default_group()
            if self.object.can_delete:
                self.object.delete()
                response['status'] = 'SUCCESS'
            else:
                response['status'] = 'ERROR'
                response['reason'] = 'FOLDER_CAN_NOT_BE_DELETED'
        else:
            response['status'] = 'ERROR'
            response['reason'] = 'OBJECT_NOT_FOUND'
        return self.ajax_response(response)


class TGFolderRenameView(LoginRequiredMixin, IsResetPasswordMixin, UpdateView):
    model = TelegramGroupOfSubscribePage
    form_class = forms.TGGroupRenameForm
    template_name = 'subscribe_pages/tg-page-list.html'
    http_method_names = ['get', 'post']

    def get_object(self, object_id: int):
        query_kwargs = {'id': int(object_id), 'user': self.request.user}

        try:
            obj = self.model.objects.get(**query_kwargs)
        except self.model.DoesNotExist:
            obj = None
        return obj

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('tg-page-list'))

    def post(self, request, *args, **kwargs):
        data = request.POST

        object_id = int(data.get('id', 0))
        self.object = self.get_object(object_id)
        object_name = data.get('name', self.object.name)

        if not self.object.can_delete:
            messages.error(self.request, 'Эту папку переименовать нельзя!')
            return HttpResponseRedirect(
                reverse_lazy('tg-page-list', args=(object_name,)))

        if self.object:
            self.object.name = object_name
            self.object.save(update_fields=['name'])
        else:
            messages.error(self.request, 'Папка не найдена!')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.path


class TGSubscribePageListView(SubscribePageListMixin):
    model = TelegramGroupOfSubscribePage
    form_class = forms.AddToTelegramFolderForm
    template_name = 'subscribe_pages/tg-page-list.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        group_name = kwargs.get('name', 'Неотсортированные')
        group = self.get_group(group_name)
        if group_name == 'Неотсортированные' and not group:
            group = self.model.objects.create(
                user=request.user,
                name='Неотсортированные',
                can_delete=False
            )
        if group_name == 'Неотсортированные' \
                and not group.tg_subscribe_pages.all() \
                and request.user.tg_group_of_pages.count() > 1:

            for page in request.user.tg_subscribe_pages.all():
                page.group = group
                page.save(update_fields=['group'])

        if not group:
            return HttpResponseRedirect(
                reverse_lazy('tg-page-list'))

        context = self.get_context_data(group=group)
        
        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        group = kwargs.get('group')
        print(group.tg_subscribe_pages)

        count_of_groups = str(self.object_list.count())
        count_of_pages = str(group.tg_subscribe_pages.count())

        context = super().get_context_data(object_list=object_list, **kwargs)

        context['groups_count'] = count_of_groups + (
            ' папка' if count_of_groups == '1' else ' папок')
        context['pages_count'] = count_of_pages + (
            ' страница' if count_of_pages == '1' else ' страниц')
        context['selected_folder_name'] = group.name
        context['TELEPORT_TG_BOT_URL'] = settings.TELEPORT_TG_BOT_URL
        context['subscribe_pages'] = group.tg_subscribe_pages.all().order_by(
            '-id')
        context['form'] = self.get_form()

        return context


class TGSubscribePageDuplicateView(LoginRequiredMixin, IsResetPasswordMixin,
                                 IsSubscribePageOwner, CreateView):
    model = TelegramSubscribePage
    queryset = TelegramSubscribePage.objects.filter(created=True)
    form_class = forms.TGSubscribePageDuplicateForm
    template_name = 'subscribe_pages/tg-page-duplicate.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_success_url(self):
        self.success_url = reverse('tg-page-detail',
                                   args=[self.object.slug])
        return str(self.success_url)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        page = get_object_or_404(TelegramSubscribePage,
                                 user=request.user, slug=kwargs.get('slug'))
        self.object = page
        self.object.slug = TelegramSubscribePage.slug_generate(
            request.user)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        context = super().get_context_data(**kwargs)
        if self.object:
            context['domain'] = self.object.domain

        context['instagram_avatar'] = self.object.get_instagram_avatar_url()
        context['domains'] = Domain.objects.filter(
            user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()

        if form.is_valid(request.user):
            page_name = form.cleaned_data['page_name'].lower()

            self.object = get_object_or_404(TelegramSubscribePage,
                                            user=request.user,
                                            slug=kwargs.get('slug'))

            # SubscribePage create
            f = form.save(commit=False)
            f.user = request.user
            f.slug = f.slug.lower()

            # copy
            f.page_name = page_name
            f.page_hash = TelegramSubscribePage.generate_page_hash(f.slug)
            f.page_photo = self.object.page_photo
            f.bg_color = self.object.bg_color
            f.description = self.object.description

            f.facebook_pixel = self.object.facebook_pixel
            f.tiktok_pixel = self.object.tiktok_pixel
            f.yandex_pixel = self.object.yandex_pixel

            if not f.instagram_avatar:
                f.instagram_avatar = self.object.instagram_avatar

            f.timer_text = self.object.timer_text
            f.is_timer_active = self.object.is_timer_active
            f.timer_time = self.object.timer_time

            f.presubscribe_text = self.object.presubscribe_text
            f.message_after_getting_present = self.object.message_after_getting_present

            f.show_subscribers = self.object.show_subscribers

            f.popup_title = self.object.popup_title
            f.popup_button_text = self.object.popup_button_text
            f.button_text = self.object.button_text
            f.button_url = self.object.button_url

            f.created = self.object.created

            return self.form_valid(form)
        else:
            return self.form_invalid(form)



class TGStatisticSubscribePageDownloadSubscribers(LoginRequiredMixin, IsResetPasswordMixin, IsSubscribePageOwner, IsSubscribePageActive, DetailView):
    model = TelegramSubscribePage
    template_name = 'subscribe_pages/tg-page-statistic.html'

    def get(self, request, *args, **kwargs):
        self.object: TelegramSubscribePage = self.get_object()
        TelegramSubscribePage.objects.filter()
        subscribers = {
            'username': [],
            'subscribed': []
        }

        for subscriber in self.object.subscribed_tg_users.all():
            if subscriber.username:
                subscribers['username'].append(subscriber.username)
                subscribers['subscribed'].append(
                    '+' if self.object in subscriber.subscribe_to.all() else '-'
                )

        excel_file_path = f'media/excels/{request.user.id}'
        if not os.path.exists(excel_file_path):
            os.makedirs(excel_file_path, exist_ok=True)
        excel_file_name = excel_file_path + f'{uuid4()}.xlsx'

        df = pd.DataFrame(subscribers)
        df.to_excel(excel_file_name, )

        with open(excel_file_name, 'rb') as f:
            response = HttpResponse(f.read())

        file_type = mimetypes.guess_type(
            excel_file_name) or 'application/octet-stream'
        response['Content-Type'] = file_type
        response['Content-Length'] = str(os.stat(excel_file_name).st_size)
        response[
            'Content-Disposition'] = "attachment; filename=subscribers.xlsx"
        os.remove(excel_file_name)
        return response


class TGStatisticAjaxView(LoginRequiredMixin, IsResetPasswordMixin, IsSubscribePageOwner, IsSubscribePageActive, DetailView, AjaxMixin):
    model = TelegramSubscribePage
    queryset = TelegramSubscribePage.objects.filter(created=True)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.get_ajax_response(views=0, subscribers=0, ctr=0)

        start_date = request.GET.get(
            'start_date',
            datetime.today() - timedelta(days=7)
        )
        end_date = request.GET.get(
            'end_date',
            datetime.today()
        )

        telegram_page_statistic_list = TelegramStatistic.objects.filter(
            telegram_subscribe_page=self.object,
            day__range=[start_date, end_date]).order_by('day')
        for page_statistic in telegram_page_statistic_list:
            response[str(page_statistic.day)] = [
                page_statistic.views,
                page_statistic.subscribers,
                page_statistic.ctr
            ]
            response['views'] += page_statistic.views
            response['subscribers'] += page_statistic.subscribers
        try:
            response['ctr'] = int(
                response['subscribers'] / response['views'] * 100
            )
        except ZeroDivisionError:
            response['ctr'] = 0
       
        return self.ajax_response(response)


class TGStatisticSubscribePageDetailView(LoginRequiredMixin, IsResetPasswordMixin, IsSubscribePageOwner, IsSubscribePageActive, DetailView):
    model = TelegramSubscribePage
    template_name = 'subscribe_pages/tg-page-statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = int(self.request.GET.get('page', 1))

        subscribers = self.object.subscribed_tg_users.all().order_by('-pk')[:100]
        print(self.object.subscribed_tg_users.all())
        paginator = Paginator(subscribers, 10)

        context['subscribers'] = paginator.get_page(page)

        context['pages'] = paginator.page_range
        context['current_page'] = page
        context['prev_page'] = page - 1 if (page - 1) in context[
            'pages'] else page
        context['next_page'] = page + 1 if (page + 1) in context[
            'pages'] else page
        return context


class TGSubscribePageCreateView(LoginRequiredMixin, IsResetPasswordMixin, CreateView):
    model = TelegramSubscribePage
    form_class = forms.TGSubscribePageCreateForm
    template_name = 'subscribe_pages/tg-page-create.html'

    def get_success_url(self):
        self.success_url = reverse('tg-page-list')
        return str(self.success_url)

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        initial = self.initial.copy()
        initial['slug'] = self.model.slug_generate(self.request.user)
        return initial

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        context = super().get_context_data(**kwargs)

        context['bg_colors'] = BGColor.objects.filter(is_active=True)

        context['domains'] = Domain.objects.filter(
            user=self.request.user)
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.page_hash = TelegramSubscribePage.generate_page_hash(f.slug)

            if not f.bg_color:
                f.bg_color = BGColor.objects.get(slug='default')

            return self.form_valid(form)
        else:
            print(form.errors.as_data())
            return self.form_invalid(form)
