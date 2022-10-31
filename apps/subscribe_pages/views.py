import os
import re
import statistics

import pandas as pd

import mimetypes

from uuid import uuid4

from celery.result import AsyncResult
from celery.schedules import timedelta

from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.generic import (
    ListView, CreateView, DetailView, DeleteView, UpdateView,
    View, TemplateView
)
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect, reverse, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.timezone import datetime
from django.utils import timezone

from rest_framework import viewsets, mixins, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

import logging
from apps.subscribe_pages.lamadava_api.lamadava import get_account_id_by_username
from apps.users.models import off_pages

# local imports
from getsub.celery import app

from apps.users.mixins import IsResetPasswordMixin

from .mixins import (
    IsSubscribePageActive, IsSubscribePageOwner,
    AjaxMixin, DeleteAjaxMixin
)
from . import models, forms, task
from .serializers import (
    VKSubscribePageSerializer, VKSubscriptionSerializer, VKSubscriberSerializer
)

from .lamadava_api.lamadava import user_is_following


logger_page = logging.getLogger('page')


# ig folders
class FolderCreateView(LoginRequiredMixin, IsResetPasswordMixin, CreateView):
    model = models.GroupOfSubscribePage
    form_class = forms.GroupCreateForm
    template_name = 'subscribe_pages/page-list.html'
    http_method_names = ['post']

    def get_success_url(self):
        return reverse_lazy('subscribe_pages:page-list',
                            args=(self.object.name,))

    def form_invalid(self, form):
        messages.error(
            self.request, 'Название папки содержит запрещенные символы'
        )
        return HttpResponseRedirect(reverse_lazy('subscribe_pages:page-list'))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            return self.form_valid(form)
        return self.form_invalid(form)


class FolderDeleteAjaxView(LoginRequiredMixin, IsResetPasswordMixin,
                           DeleteAjaxMixin):
    model = models.GroupOfSubscribePage
    id_field_name = 'folderID'
    is_owner = True

    def delete(self, request, *args, **kwargs):
        response = self.get_ajax_response()
        data = request.POST
        object_id = int(data.get(self.id_field_name, 0))

        self.object: models.GroupOfSubscribePage = self.get_object(object_id)
        if self.object:
            for subscribe_page in self.object.subscribe_pages.all():
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


class FolderRenameView(LoginRequiredMixin, IsResetPasswordMixin, UpdateView):
    model = models.GroupOfSubscribePage
    form_class = forms.GroupRenameForm
    template_name = 'subscribe_pages/page-list.html'
    http_method_names = ['get', 'post']

    def get_object(self, object_id: int):
        query_kwargs = {'id': int(object_id), 'user': self.request.user}

        try:
            obj = self.model.objects.get(**query_kwargs)
        except self.model.DoesNotExist:
            obj = None
        return obj

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('subscribe_pages:page-list'))

    def post(self, request, *args, **kwargs):
        data = request.POST

        object_id = int(data.get('id', 0))
        self.object = self.get_object(object_id)
        object_name = data.get('name', self.object.name)

        if not self.object.can_delete:
            messages.error(self.request, 'Эту папку переименовать нельзя!')
            return HttpResponseRedirect(
                reverse_lazy('subscribe_pages:page-list', args=(object_name,)))

        if self.object:
            self.object.name = object_name
            self.object.save(update_fields=['name'])
        else:
            messages.error(self.request, 'Папка не найдена!')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.path


class AddToFolderView(LoginRequiredMixin, AjaxMixin, View):
    def post(self, request, *args, **kwargs):
        response = self.get_ajax_response()
        data = request.POST
        page = models.InstagramSubscribePage.objects.get(
            slug=data['slug'], user=request.user
        )
        group = models.GroupOfSubscribePage.objects.get(
            user=request.user, id=int(data['group_id'])
        )
        page.group = group
        page.save()
        response['status'] = 'SUCCESS'
        response['url'] = '/subscribe-pages/%s/' % group.name

        return self.ajax_response(response)


# ig subscribe pages - crud
class SubscribePageListView(LoginRequiredMixin, IsResetPasswordMixin, ListView,
                            FormMixin):
    model = models.GroupOfSubscribePage
    context_object_name = 'folder_list'
    template_name = 'subscribe_pages/page-list.html'
    form_class = forms.AddToFolderForm

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        group_name = kwargs.get('name', 'Неотсортированные')
        group = self.get_group(group_name)
        # models.InstagramSubscribePage.activate_user_subscribe_pages(request.user)

        # print(group.subscribe_pages.all()[0])

        if group_name == 'Неотсортированные' and not group:
            group = models.GroupOfSubscribePage.objects.create(
                user=request.user,
                name='Неотсортированные',
                can_delete=False
            )
        if group_name == 'Неотсортированные' \
                and not group.subscribe_pages.all() \
                and request.user.group_of_pages.all().count() > 1:

            for page in request.user.subscribe_pages.all():
                page.group = group
                page.save(update_fields=['group'])

        if not group:
            return HttpResponseRedirect(
                reverse_lazy('subscribe_pages:page-list'))

        context = self.get_context_data(group=group)
        
        return self.render_to_response(context)

    def get_group(self, group_name: str):
        group_list = self.object_list.filter(name=group_name)

        if not group_list:
            group = None
        else:
            group = group_list[0]

        return group

    def get_context_data(self, *, object_list=None, **kwargs):
        group = kwargs.get('group')

        count_of_groups = str(self.object_list.count())
        count_of_pages = str(group.subscribe_pages.count())

        context = super().get_context_data(object_list=object_list, **kwargs)

        context['groups_count'] = count_of_groups + (
            ' папка' if count_of_groups == '1' else ' папок')
        context['pages_count'] = count_of_pages + (
            ' страница' if count_of_pages == '1' else ' страниц')
        context['selected_folder_name'] = group.name
        context['subscribe_pages'] = group.subscribe_pages.all().order_by(
            '-id')
        context['form'] = self.get_form()

        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class SubscribePageCreateView(LoginRequiredMixin, IsResetPasswordMixin,
                              CreateView):
    model = models.InstagramSubscribePage
    form_class = forms.SubscribePageCreateForm
    template_name = 'subscribe_pages/page-create.html'

    def get_success_url(self):
        self.success_url = reverse('subscribe_pages:page-list')
        return str(self.success_url)

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        initial = self.initial.copy()
        initial['slug'] = self.model.slug_generate(self.request.user)
        return initial

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        context = super().get_context_data(**kwargs)

        context['bg_colors'] = models.BGColor.objects.filter(is_active=True)

        context['domains'] = models.Domain.objects.filter(
            user=self.request.user)
        return context

    def form_valid(self, form):
        self.object = form.save()

        task.save_instagram_info.delay(
            self.object.pk)  # сохраняем инфу о аккаунте в подписную страницу

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        if form.is_valid():
            instagram_username = form.cleaned_data[
                'instagram_username']

            instagram_user_info = form.instagram_user_info

            f = form.save(commit=False)
            f.user = request.user
            f.instagram_username = instagram_username
            f.instagram_name = instagram_username

            if instagram_user_info.get("follower_count"):
                f.follower_count = instagram_user_info["follower_count"]
                f.following_count = instagram_user_info["following_count"]
                f.media_count = instagram_user_info["media_count"]

            if not f.bg_color:
                f.bg_color = models.BGColor.objects.get(slug='default')

            models.InstagramCreator.objects.get_or_create(user=request.user,
                                                          instagram=instagram_username)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SubscribePageCreateSlugCheckAjaxView(LoginRequiredMixin,
                                           IsResetPasswordMixin, View,
                                           AjaxMixin):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        response = self.get_ajax_response()
        slug = request.POST.get('slug')

        if models.InstagramSubscribePage.is_slug_unique(slug):
            response['is_unique'] = True
        else:
            response['is_unique'] = False
            response['error'] = 'Страница с такой ссылкой уже существует'
        return self.ajax_response(response)


class SubscribePageDetailView(LoginRequiredMixin, IsResetPasswordMixin,
                              IsSubscribePageOwner, UpdateView):
    model = models.InstagramSubscribePage
    form_class = forms.SubscribePageUpdateForm
    template_name = 'subscribe_pages/page-detail.html'
    success_url = reverse_lazy('subscribe_pages:page-list')

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

        # s = self.get_object()

        context['domain'] = self.object.domain
        context['domains'] = models.Domain.objects.filter(
            user=self.request.user)

        context['bg_color'] = self.object.bg_color
        context['bg_colors'] = models.BGColor.objects.filter(is_active=True)

        context['page_photo'] = f'https://{self.object.get_page_photo_url()}'
        context['instagram_avatar'] = self.object.get_instagram_avatar_url()
        context['instagram_username'] = self.object.instagram_username
        context["follower_count"] = 1000

        return context

    def form_valid(self, form):
        self.object = form.save()
        task.save_instagram_info.delay(
            self.object.pk)  # сохраняем инфу о аккаунте в подписную страницу

        return super().form_valid(form)


class SubscribePageDetailSlugCheckAjaxView(LoginRequiredMixin,
                                           IsResetPasswordMixin,
                                           IsSubscribePageOwner,
                                           IsSubscribePageActive, DetailView,
                                           AjaxMixin):
    model = models.InstagramSubscribePage
    queryset = models.InstagramSubscribePage.objects.filter(created=True)
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.get_ajax_response()

        slug = request.POST.get('slug')

        if slug == self.object.slug:
            response['is_unique'] = True
        else:
            if models.InstagramSubscribePage.is_slug_unique(slug):
                response['is_unique'] = True
            else:
                response['is_unique'] = False
                response['error'] = 'Страница с такой ссылкой уже существует'
        return self.ajax_response(response)


class SubscribePageDuplicateView(LoginRequiredMixin, IsResetPasswordMixin,
                                 IsSubscribePageOwner, CreateView):
    model = models.InstagramSubscribePage
    queryset = models.InstagramSubscribePage.objects.filter(created=True)
    form_class = forms.SubscribePageDuplicateForm
    template_name = 'subscribe_pages/page-duplicate.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_success_url(self):
        self.success_url = reverse('subscribe_pages:page-detail',
                                   args=[self.object.slug])
        return str(self.success_url)

    def form_valid(self, form):
        self.object = form.save()
        task.save_instagram_info.delay(
            self.object.pk)  # сохраняем инфу о аккаунте в подписную страницу
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        page = get_object_or_404(models.InstagramSubscribePage,
                                 user=request.user, slug=kwargs.get('slug'))
        self.object = page
        self.object.slug = models.InstagramSubscribePage.slug_generate(
            request.user)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        context = super().get_context_data(**kwargs)
        if self.object:
            context['domain'] = self.object.domain

        context['instagram_avatar'] = self.object.get_instagram_avatar_url()
        context['domains'] = models.Domain.objects.filter(
            user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()

        if form.is_valid(request.user):
            instagram_username = form.cleaned_data[
                'instagram_username'].lower().strip().replace('@', '')
            page_name = form.cleaned_data['page_name'].lower()

            self.object = get_object_or_404(models.InstagramSubscribePage,
                                            user=request.user,
                                            slug=kwargs.get('slug'))

            # SubscribePage create
            f = form.save(commit=False)
            f.user = request.user
            f.slug = f.slug.lower()
            f.instagram_username = instagram_username

            # copy
            f.page_name = page_name
            f.page_photo = self.object.page_photo
            f.bg_color = self.object.bg_color

            f.title = self.object.title
            f.description = self.object.description
            f.button_text = self.object.button_text

            f.facebook_pixel = self.object.facebook_pixel
            f.tiktok_pixel = self.object.tiktok_pixel
            f.yandex_pixel = self.object.yandex_pixel

            if not f.instagram_avatar:
                f.instagram_avatar = self.object.instagram_avatar

            f.timer_text = self.object.timer_text
            f.is_timer_active = self.object.is_timer_active
            f.timer_time = self.object.timer_time

            f.presubscribe_text = self.object.presubscribe_text
            f.precheck_subscribe_text = self.object.precheck_subscribe_text

            f.enter_login_placeholder = self.object.enter_login_placeholder
            f.help_text = self.object.help_text

            f.subscribe_button = self.object.subscribe_button
            f.already_subscribed_text = self.object.already_subscribed_text

            f.subscribed_button = self.object.subscribed_button
            f.not_yet_subscribed = self.object.not_yet_subscribed

            f.presearch_text = self.object.presearch_text
            f.search_text = self.object.search_text
            f.search_time_text = self.object.search_time_text
            f.success_text = self.object.success_text
            f.error_text = self.object.error_text

            f.single_page = self.object.single_page
            f.show_subscribers = self.object.show_subscribers

            f.popup_title = self.object.popup_title
            f.popup_text = self.object.popup_text
            f.popup_button_url = self.object.popup_button_url

            f.created = self.object.created

            models.InstagramCreator.objects.get_or_create(user=request.user,
                                                          instagram=instagram_username)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class StatisticSubscribePageDetailView(LoginRequiredMixin,
                                       IsResetPasswordMixin,
                                       IsSubscribePageOwner,
                                       IsSubscribePageActive, DetailView):
    model = models.InstagramSubscribePage
    template_name = 'subscribe_pages/page-statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = int(self.request.GET.get('page', 1))

        subscribers = self.object.views.exclude(instagram_username='').filter(
            instagram_username__isnull=False
        ).order_by('-date')[:100]
        paginator = Paginator(subscribers, 10)

        context['subscribers'] = paginator.get_page(page)

        context['pages'] = paginator.page_range
        context['current_page'] = page
        context['prev_page'] = page - 1 if (page - 1) in context[
            'pages'] else page
        context['next_page'] = page + 1 if (page + 1) in context[
            'pages'] else page
        return context


class SearchSubscribersAjaxView(LoginRequiredMixin, IsResetPasswordMixin,
                                IsSubscribePageOwner, IsSubscribePageActive,
                                DetailView, AjaxMixin):
    model = models.InstagramSubscribePage
    template_name = 'subscribe_pages/page-statistic.html'

    def get(self, request, *args, **kwargs):
        response = self.get_ajax_response(subscribers=[])

        data = request.GET

        instagram_username = data.get('instagram_username')
        subscribers = models.InstagramSubscriber.objects.filter(
            instagram_username__startswith=instagram_username)[:100]

        for subscriber in subscribers:
            response['subscribers'].append(
                {
                    'date': subscriber.date.strftime('%d.%m.%Y %H:%M'),
                    'username': subscriber.instagram_username,
                    'subscribed': subscriber.can_get_material
                }
            )
        return self.ajax_response(response)


class StatisticSubscribePageDownloadSubscribers(LoginRequiredMixin,
                                                IsResetPasswordMixin,
                                                IsSubscribePageOwner,
                                                IsSubscribePageActive,
                                                DetailView):
    model = models.InstagramSubscribePage
    template_name = 'subscribe_pages/page-statistic.html'

    def get(self, request, *args, **kwargs):
        self.object: models.InstagramSubscribePage = self.get_object()
        models.InstagramSubscribePage.objects.filter()
        subscribers = {
            'username': [],
            'subscribed': []
        }

        for subscriber in self.object.views.all():
            # subscribers['date'].append(str(subscriber.date))
            if subscriber.instagram_username:
                subscribers['username'].append(subscriber.instagram_username)
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


class StatisticAjaxView(LoginRequiredMixin, IsResetPasswordMixin,
                        IsSubscribePageOwner, IsSubscribePageActive,
                        DetailView, AjaxMixin):
    model = models.InstagramSubscribePage
    queryset = models.InstagramSubscribePage.objects.filter(created=True)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.get_ajax_response(views=0, subscribers=0, ctr=0)

        start_date = request.GET.get('start_date',
                                     datetime.today() - timedelta(days=7))
        end_date = request.GET.get('end_date', datetime.today())

        page_statistic_list = models.InstagramStatistic.objects.filter(
            subscribe_page=self.object,
            day__range=[start_date, end_date]).order_by('day')
        for page_statistic in page_statistic_list:
            response[str(page_statistic.day)] = [page_statistic.views,
                                                 page_statistic.subscribers,
                                                 page_statistic.ctr]
            response['views'] += page_statistic.views
            response['subscribers'] += page_statistic.subscribers
        try:
            response['ctr'] = int(
                response['subscribers'] / response['views'] * 100)
        except ZeroDivisionError:
            response['ctr'] = 0
       
        return self.ajax_response(response)


class SubscribePageDeleteView(LoginRequiredMixin, IsResetPasswordMixin,
                              DeleteAjaxMixin):
    model = models.InstagramSubscribePage
    id_field_name = 'pageID'
    is_owner = True


# ig subscribe pages
class SubscribePageOpenView(IsSubscribePageActive, DetailView):
    model = models.InstagramSubscribePage
    queryset = models.InstagramSubscribePage.objects.filter(created=True)
    template_name = 'subscribe_pages/page-open.html'
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
            # self.object.user.pocket.pay_per_subscriber()
            subscriber = models.InstagramSubscriber.get_or_create_by_user_ip(
                request)

            statistic, statistic_created = models.InstagramStatistic.objects.get_or_create(
                        subscribe_page=self.object, day=datetime.today())

            if not subscriber.is_visited_page_by_slug(
                    self.object.slug):  # Если он не был на этой странице то
                try:
                    # получаем/создаём статистику сегодняшнего дня
                    statistic, statistic_created = models.InstagramStatistic.objects.get_or_create(
                        subscribe_page=self.object, day=datetime.today())

                except models.InstagramStatistic.MultipleObjectsReturned:
                    statistics = models.InstagramStatistic.objects.filter(
                        subscribe_page=self.object, day=datetime.today())
                    statistic = statistics[0]
                    for statistic_ in statistics[1:]:
                        statistic.views += statistic_.views
                        statistic_.delete()

                statistic.views += 1
                statistic.save(update_fields=['views'])
                subscriber.views.add(
                    self.object)  # добавляем страницу в просмотренные
        except Exception as e:
            logger_page.warning(
                f'\n{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}: '
                f'error: {e}, '
                f'slug: {self.object.slug}, '
                f'ip: {request.META}')

        if self.object.single_page:
            return redirect(
                reverse_lazy(
                    'subscribe_pages:page-get_material',
                    args=(self.object.slug,)
                )
            )

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class SubscribePageGetMaterials(IsSubscribePageActive, FormMixin, DetailView):
    http_method_names = ['get', 'post']
    model = models.InstagramSubscribePage
    queryset = models.InstagramSubscribePage.objects.filter(created=True)
    form_class = forms.InstagramLoginForm
    template_name = 'subscribe_pages/page-subscribe.html'
    context_object_name = 'page'

    def is_instagram_browser(self):
        return 'Instagram' in self.request.headers['User-Agent']

    def is_mobile_browser(self):
        return 'Mobile' in self.request.headers['User-Agent']

    def get_success_url(self):
        self.success_url = reverse_lazy('subscribe_pages:check-username',
                                        args=[self.object.slug])
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['bg_color'] = self.object.bg_color

        context['instagram_url'] = (
            f'https://instagram.com/{self.object.instagram_username}/' if self.is_instagram_browser() else
            f'instagram://user?username={self.object.instagram_username}' if self.is_mobile_browser() else
            f'https://instagram.com/{self.object.instagram_username}/'
        )

        context['show_subscribes'] = self.object.show_subscribers
        context['follower_count'] = self.object.follower_count
        context['following_count'] = self.object.following_count
        context['media_count'] = self.object.media_count
        context['instagram_avatar'] = self.object.get_instagram_avatar_url()

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            subscriber = models.InstagramSubscriber.get_or_create_by_user_ip(
                request)
            if not subscriber.is_visited_page_by_slug(
                    self.object.slug):  # Если он не был на этой странице то
                try:
                    # получаем/создаём статистику сегодняшнего дня
                    statistic, statistic_created = models.InstagramStatistic.objects.get_or_create(
                        subscribe_page=self.object, day=datetime.today())

                except models.InstagramStatistic.MultipleObjectsReturned:
                    statistics = models.InstagramStatistic.objects.filter(
                        subscribe_page=self.object, day=datetime.today())
                    statistic = statistics[0]
                    for statistic_ in statistics[1:]:
                        logger_page.warning(
                            f'\n{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}: old: {statistic_.views}, new: {statistic.views}'
                        )
                        statistic.views += statistic_.views
                        statistic_.delete()

                statistic.views += 1
                statistic.save(update_fields=['views'])
                subscriber.views.add(
                    self.object)  # добавляем страницу в просмотренные
        except Exception as e:
            logger_page.warning(
                f'\n{timezone.now().strftime("%Y-%m-%d %H:%M:%S")}: '
                f'error: {e}, '
                f'slug: {self.object.slug}, '
                f'ip: {request.META}')

        context = self.get_context_data(object=self.object)

        return self.render_to_response(context)


class SubscribePageAjaxCheckUsername(IsSubscribePageActive, DetailView,
                                     AjaxMixin):
    http_method_names = ['post']
    model = models.InstagramSubscribePage
    queryset = models.InstagramSubscribePage.objects.filter(created=True)

    def post(self, request, *args, **kwargs):
        # print()
        instagram_username = self.get_object().__dict__["instagram_username"]
        username2 = request.POST.get("login", "")

        n = user_is_following(instagram_username, username2)

        if not n:
            return HttpResponse("FAIL")

        s = False

        try:
            for i in n:
                if i.get("username") == username2:
                    s = True
                    break
        except:
            pass

        page = self.get_object()

        if not s or page.user.pocket.balance <= 0:
            return HttpResponse("FAIL")

        subscriber = models.InstagramSubscriber.get_or_create_by_user_ip(request)
        if subscriber.is_visited_page_by_slug(self.object.slug):
            return HttpResponse("FAIL")

        page.user.pocket.pay_per_subscriber()
        statistic, statistic_created = models.InstagramStatistic.objects.get_or_create(
                        subscribe_page=self.object, day=datetime.today())

        statistic.subscribers += 1
        statistic.save(update_fields=["subscribers"])

        subscriber.instagram_username = username2
        subscriber.subscribe_to.add(page)
        subscriber.save()

        return HttpResponse("SUCCESS")


class SubscribePageSuccessView(IsSubscribePageActive, DetailView):
    model = models.InstagramSubscribePage
    template_name = 'subscribe_pages/page-success.html'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['bg_color'] = self.object.bg_color
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.single_page:
            return redirect(self.object.popup_button_url)

        context = self.get_context_data(object=self.object)
        
        return self.render_to_response(context)


# vk subscribe pages - crud
class VKSubscribePageListView(LoginRequiredMixin, IsResetPasswordMixin,
                              ListView, FormMixin):
    model = models.VKGroupOfSubscribePage
    context_object_name = 'folder_list'
    template_name = 'subscribe_pages/vk-page-list.html'
    form_class = forms.VKAddToFolderForm

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        group_name = kwargs.get('name', 'Неотсортированные')
        group = self.get_group(group_name)
        if group_name == 'Неотсортированные' and not group:
            group = models.VKGroupOfSubscribePage.objects.create(
                user=request.user,
                name='Неотсортированные',
                can_delete=False
            )

        if not group:
            return HttpResponseRedirect(
                reverse_lazy('subscribe_pages:vk-page-list'))

        context = self.get_context_data(group=group)
        return self.render_to_response(context)

    def get_group(self, group_name: str):
        group_list = self.object_list.filter(name=group_name)
        if not group_list:
            group = None
        else:
            group = group_list[0]
        return group

    def get_context_data(self, *, object_list=None, **kwargs):
        group = kwargs.get('group')

        count_of_groups = str(self.object_list.count())
        count_of_pages = str(group.vk_subscribe_pages.count())

        context = super().get_context_data(object_list=object_list, **kwargs)

        context['groups_count'] = count_of_groups + (
            ' папка' if count_of_groups == '1' else ' папок')
        context['pages_count'] = count_of_pages + (
            ' страница' if count_of_pages == '1' else ' страниц')
        context['selected_folder_name'] = group.name
        context[
            'vk_subscribe_pages'] = group.vk_subscribe_pages.all().order_by(
            '-id')
        context['form'] = self.get_form()

        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class VKSubscribePageCreateView(LoginRequiredMixin, IsResetPasswordMixin,
                                CreateView):
    model = models.VKSubscribePage
    form_class = forms.VKSubscribePageCreateForm
    template_name = 'subscribe_pages/vk-page-create.html'

    def get_success_url(self):
        self.success_url = reverse('subscribe_pages:vk-page-list')
        return str(self.success_url)

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        initial = self.initial.copy()
        initial['slug'] = self.model.slug_generate(self.request.user)
        return initial

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        context = super().get_context_data(**kwargs)

        context['bg_colors'] = models.BGColor.objects.filter(is_active=True)

        context['domains'] = models.Domain.objects.filter(
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
            if not f.bg_color:
                f.bg_color = models.BGColor.objects.get(slug='default')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class VKSubscribePageCreateSlugCheckAjaxView(LoginRequiredMixin,
                                             IsResetPasswordMixin, View,
                                             AjaxMixin):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        response = self.get_ajax_response()
        slug = request.POST.get('slug')

        if models.VKSubscribePage.is_slug_unique(slug):
            response['is_unique'] = True
        else:
            response['is_unique'] = False
            response['error'] = 'Страница с такой ссылкой уже существует'
        return self.ajax_response(response)


class VKSubscribePageDetailView(LoginRequiredMixin, IsResetPasswordMixin,
                                IsSubscribePageOwner, UpdateView):
    model = models.VKSubscribePage
    form_class = forms.VKSubscribePageUpdateForm
    template_name = 'subscribe_pages/vk-page-detail.html'
    success_url = reverse_lazy('subscribe_pages:vk-page-list')

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

        context['bg_color'] = self.object.bg_color
        context['bg_colors'] = models.BGColor.objects.filter(is_active=True)

        context['page_photo'] = f'https://{self.object.get_page_photo_url()}'
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class VKSubscribePageDetailSlugCheckAjaxView(LoginRequiredMixin,
                                             IsResetPasswordMixin,
                                             IsSubscribePageOwner,
                                             IsSubscribePageActive, DetailView,
                                             AjaxMixin):
    model = models.VKSubscribePage
    queryset = models.VKSubscribePage.objects.filter(created=True)
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.get_ajax_response()

        slug = request.POST.get('slug')

        if slug == self.object.slug:
            response['is_unique'] = True
        else:
            if models.VKSubscribePage.is_slug_unique(slug):
                response['is_unique'] = True
            else:
                response['is_unique'] = False
                response['error'] = 'Страница с такой ссылкой уже существует'
        return self.ajax_response(response)


class VKSubscribePageDuplicateView(LoginRequiredMixin, IsResetPasswordMixin,
                                   IsSubscribePageOwner, CreateView):
    model = models.VKSubscribePage
    queryset = models.VKSubscribePage.objects.filter(created=True)
    form_class = forms.VKSubscribePageDuplicateForm
    template_name = 'subscribe_pages/vk-page-duplicate.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_success_url(self):
        self.success_url = reverse('subscribe_pages:vk-page-detail',
                                   args=[self.object.slug])
        return str(self.success_url)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        page = get_object_or_404(models.VKSubscribePage, user=request.user,
                                 slug=kwargs.get('slug'))
        self.object = page
        self.object.slug = models.VKSubscribePage.slug_generate(request.user)
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()

        if form.is_valid(request.user):
            page_name = form.cleaned_data['page_name'].lower()

            self.object = get_object_or_404(models.VKSubscribePage,
                                            user=request.user,
                                            slug=kwargs.get('slug'))

            # SubscribePage create
            f = form.save(commit=False)
            f.user = request.user
            f.slug = f.slug.lower()

            # copy
            f.page_name = page_name
            f.page_photo = self.object.page_photo
            f.bg_color = self.object.bg_color

            f.title = self.object.title
            f.description = self.object.description
            f.button_text = self.object.button_text

            f.timer_text = self.object.timer_text
            f.is_timer_active = self.object.is_timer_active
            f.timer_time = self.object.timer_time

            f.success_title = self.object.success_title
            f.success_text = self.object.success_text
            f.success_button_url = self.object.success_button_url
            f.success_button_text = self.object.success_button_text

            f.created = self.object.created
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class VKStatisticSubscribePageDetailView(
    LoginRequiredMixin, IsResetPasswordMixin, IsSubscribePageOwner,
    IsSubscribePageActive, DetailView):
    model = models.VKSubscribePage
    template_name = 'subscribe_pages/vk-page-statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = int(self.request.GET.get('page', 1))

        subscribers = self.object.subscriptions.all().order_by('-date')[:100]

        paginator = Paginator(subscribers, 10)

        context['subscribers'] = paginator.get_page(page)

        context['pages'] = paginator.page_range
        context['current_page'] = page
        context['prev_page'] = page - 1 if (page - 1) in context[
            'pages'] else page
        context['next_page'] = page + 1 if (page + 1) in context[
            'pages'] else page
        return context


class VKSearchSubscribersAjaxView(LoginRequiredMixin, IsResetPasswordMixin,
                                  IsSubscribePageOwner, IsSubscribePageActive,
                                  DetailView, AjaxMixin):
    model = models.VKSubscribePage
    template_name = 'subscribe_pages/vk-page-statistic.html'

    def get(self, request, *args, **kwargs):
        response = self.get_ajax_response(subscribers=[])

        data = request.GET

        self.object = self.get_object()

        first_name = data.get('instagram_username')
        subscribers = self.object.subscriptions.objects.filter(
            vk_subscriber__first_name__startswith=first_name)[:100]

        for subscriber in subscribers:
            response['subscribers'].append(
                {
                    'date': subscriber.date.strftime('%d.%m.%Y %H:%M'),
                    'first_name': subscriber.first_name,
                    'subscribed': subscriber.can_get_material
                }
            )
        return self.ajax_response(response)


class VKStatisticSubscribePageDownloadSubscribers(
    LoginRequiredMixin,
    IsResetPasswordMixin, IsSubscribePageOwner, IsSubscribePageActive,
    DetailView
):
    model = models.VKSubscribePage
    template_name = 'subscribe_pages/vk-page-statistic.html'

    def get(self, request, *args, **kwargs):
        self.object: models.VKSubscribePage = self.get_object()
        models.VKSubscribePage.objects.filter()
        subscribers = {
            # 'date': [],
            'username': [],
            'subscribed': []
        }

        for subscriber in self.object.views.all():
            # subscribers['date'].append(str(subscriber.date))
            subscribers['username'].append(subscriber.instagram_username)
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


class VKStatisticAjaxView(LoginRequiredMixin, IsResetPasswordMixin,
                          IsSubscribePageOwner, IsSubscribePageActive,
                          DetailView, AjaxMixin):
    model = models.VKSubscribePage
    queryset = models.VKSubscribePage.objects.filter(created=True)
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = self.get_ajax_response(views=0, subscribers=0, ctr=0)
        today = datetime.today()

        start_date = request.GET.get('start_date', today - timedelta(days=7))
        end_date = request.GET.get('end_date', today)

        page_subscriptions = self.object.subscriptions.filter(
            date__range=[start_date, end_date]
        ).order_by('date')

        views = page_subscriptions.count()
        subscribers = page_subscriptions.filter(subscribed=True).count()
        try:
            ctr = subscribers / views * 100
        except ZeroDivisionError:
            ctr = 0

        day_views = 0
        day_subscribers = 0
        day_ctr = 0
        for page_subscription in page_subscriptions:

            date = str(page_subscription.date.strftime('%m.%d.%Y'))
            if not response.get(date):
                response[date] = []

                day_views = 0
                day_subscribers = 0
                day_ctr = 0

            day_views += 1
            day_subscribers += 1 if page_subscription.subscribed else 0
            try:
                day_ctr = day_subscribers / day_views * 100
            except ZeroDivisionError:
                day_ctr = 0

            response[date] = [day_views, day_subscribers, day_ctr]

        response['views'] += views
        response['subscribers'] += subscribers
        response['ctr'] += ctr
        return self.ajax_response(response)


class VKSubscribePageDeleteView(LoginRequiredMixin, IsResetPasswordMixin,
                                DeleteAjaxMixin):
    model = models.VKSubscribePage
    id_field_name = 'pageID'
    is_owner = True


# vk folders
class VKFolderCreateView(LoginRequiredMixin, IsResetPasswordMixin, CreateView):
    model = models.VKGroupOfSubscribePage
    form_class = forms.VKGroupCreateForm
    template_name = 'subscribe_pages/vk-page-list.html'
    http_method_names = ['post']

    def get_success_url(self):
        return reverse_lazy('subscribe_pages:vk-page-list',
                            args=(self.object.name,))

    def form_invalid(self, form):
        messages.error(
            self.request, 'Название папки содержит запрещенные символы'
        )
        return HttpResponseRedirect(reverse_lazy('subscribe_pages:page-list'))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            return self.form_valid(form)
        return self.form_invalid(form)


class VKFolderDeleteAjaxView(LoginRequiredMixin, IsResetPasswordMixin,
                             DeleteAjaxMixin):
    model = models.VKGroupOfSubscribePage
    id_field_name = 'folderID'
    is_owner = True

    def delete(self, request, *args, **kwargs):
        response = self.get_ajax_response()
        data = request.POST
        object_id = int(data.get(self.id_field_name, 0))

        self.object: models.VKGroupOfSubscribePage = self.get_object(object_id)
        if self.object:
            for subscribe_page in self.object.vk_subscribe_pages.all():
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


class VKFolderRenameView(LoginRequiredMixin, IsResetPasswordMixin, UpdateView):
    model = models.VKGroupOfSubscribePage
    form_class = forms.VKGroupRenameForm
    template_name = 'subscribe_pages/vk-page-list.html'
    http_method_names = ['get', 'post']

    def get_object(self, **kwargs):
        object_id = int(self.request.POST.get('id', 0))
        query_kwargs = {'id': int(object_id), 'user': self.request.user}

        try:
            obj = self.model.objects.get(**query_kwargs)
        except self.model.DoesNotExist:
            obj = None
        return obj

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(
            reverse_lazy('subscribe_pages:vk-page-list'))

    def post(self, request, *args, **kwargs):
        data = request.POST

        self.object = self.get_object(**kwargs)
        object_name = data.get('name', self.object.name)

        if not self.object.can_delete:
            messages.error(self.request, 'Эту папку переименовать нельзя!')
            return HttpResponseRedirect(
                reverse_lazy(
                    'subscribe_pages:page-list',
                    args=(object_name,)
                )
            )

        if self.object:
            self.object.name = object_name
            self.object.save(update_fields=['name'])
        else:
            messages.error(self.request, 'Папка не найдена!')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.path


class AddToVKFolderView(LoginRequiredMixin, AjaxMixin, View):
    def post(self, request, *args, **kwargs):
        response = self.get_ajax_response()
        data = request.POST
        try:
            page = models.VKSubscribePage.objects.get(
                slug=data['slug'], user=request.user
            )
            group = models.VKGroupOfSubscribePage.objects.get(
                user=request.user, id=int(data['group_id'])
            )
            page.group = group
            page.save(update_fields=['group'])
            response['status'] = 'SUCCESS'
            response['url'] = '/vk-subscribe-pages/%s/' % group.name
        except:
            response['status'] = 'FAIL'

        return self.ajax_response(response)


# domains
class DomainCreateListView(LoginRequiredMixin, IsResetPasswordMixin,
                           CreateView, ListView):
    model = models.Domain
    queryset = model.objects.filter(for_delete=False)
    form_class = forms.DomainCreateForm

    template_name = 'subscribe_pages/domain.html'

    success_url = reverse_lazy('subscribe_pages:domain-list')

    context_object_name = 'domain_list'

    def form_valid(self, form):
        self.object = form.save()
        task.domain_add.delay(self.object.domain)
        return super().form_valid(form)

    def get_queryset(self, ):
        return self.queryset.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        form = self.get_form()
        # return self.form_invalid(form)
        if form.is_valid(request.user):
            f = form.save(commit=False)
            f.domain = f.domain.replace(
                'http://', ''
            ).replace(
                'https://', ''
            ).replace(
                '/', ''
            ).strip()

            f.user = request.user
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DomainDeleteAjaxView(LoginRequiredMixin, IsResetPasswordMixin,
                           DeleteAjaxMixin):
    model = models.Domain
    id_field_name = 'domainID'
    is_owner = True


class DomainInstructionTemplateView(LoginRequiredMixin, IsResetPasswordMixin,
                                    TemplateView):
    template_name = 'subscribe_pages/instructions.html'


# API
class VKSubscribePageViewSet(mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    queryset = models.VKSubscribePage.objects.all()
    serializer_class = VKSubscribePageSerializer
    lookup_field = 'slug'


class VKSubscriberViewSet(mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    queryset = models.VKSubscriber.objects.all()
    serializer_class = VKSubscriberSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform
        filter_kwargs = {
            'vk_user_id': self.request.data.get('vk_user_id'),
        }
        try:
            obj = queryset.get(**filter_kwargs)
        except models.VKSubscriber.DoesNotExist:
            obj = None
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object:
            return self.update(request, *args, **kwargs)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class VKStatisticAPIView(generics.CreateAPIView, mixins.UpdateModelMixin):
    queryset = models.VKSubscription.objects.all()
    serializer_class = VKSubscriptionSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform
        filter_kwargs = {
            'vk_subscriber': self.request.data.get('vk_subscriber'),
            'vk_page': self.request.data.get('vk_page')
        }
        try:
            obj = queryset.get(**filter_kwargs)
        except models.VKSubscription.DoesNotExist:
            obj = None
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object:
            return self.update(request, *args, **kwargs)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)