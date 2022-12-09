from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import datetime
from .lamadava_api.lamadava import get_instagram_profile_data_by_username

import re

import socket

import logging

# local imports
from . import models


loggerDomain = logging.getLogger('domain')


# ig folders
class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = models.GroupOfSubscribePage
        fields = ['name']

    def is_valid(self):
        name = self.data.get('name')
        forbidden_characters = set(re.findall('[^\daA-zZаА-яЯ\.-]', name))

        if forbidden_characters:
            forbidden_characters = list(
                map(lambda x: f'"{x}"', forbidden_characters))
            self.add_error('name', 'Название содержит запрещённые символы:')
            self.add_error('name', ', '.join(forbidden_characters))
        return self.is_bound and not self.errors


class GroupRenameForm(forms.ModelForm):
    class Meta:
        model = models.GroupOfSubscribePage
        fields = ['name']


class AddToFolderForm(forms.ModelForm):
    def is_valid(self, user):
        slug = self.data.get('slug')

        exist = models.InstagramSubscribePage.objects.filter(user=user, slug=slug)
        if not exist:
            self.add_error('slug', 'Не удалось найти страницу')

        return super().is_valid()

    class Meta:
        model = models.InstagramSubscribePage
        fields = ['slug', 'group']
        widgets = {
            'slug': forms.HiddenInput(attrs={
                'class': 'AddToFolder',
                'id': 'page_slug'
            }),
            'group': forms.HiddenInput(attrs={
                'class': 'AddToFolder',
                'id': 'folder_id'
            }),
        }


# ig subscribe pages
class SubscribePageCreateForm(forms.ModelForm):
    def is_valid(self):
        slug = self.data.get('slug').lower()
        popup_button_url = self.data.get('popup_button_url')
        page_photo = self.files.get('page_photo')
        instagram_username = str(self.data.get('instagram_username')).replace('@', '').strip().lower()

        if not instagram_username:
            self.add_error('instagram_username', 'Введите ник')
            self.fields['instagram_username'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        else:
            instagram_user_info = get_instagram_profile_data_by_username(instagram_username) # проверка профиля

            if instagram_user_info.get("exc_type") == "UserNotFound":  # если аккаунт не найден
                self.add_error('instagram_username', 'Аккаунт не найден')
                self.fields['instagram_username'].widget.attrs.update({
                    'class': 'sheet_input error'
                })

            elif instagram_user_info.get("exc_type"):  # если аккаунт не найден
                self.add_error('instagram_username', 'Произошла ошибка, попробуйте ещё раз')
                self.fields['instagram_username'].widget.attrs.update({
                    'class': 'sheet_input error'
                })

            if instagram_user_info.get('is_private'):  # если аккаунт приватный
                self.add_error('instagram_username', 'Аккаунт приватный')
                self.fields['instagram_username'].widget.attrs.update({
                    'class': 'sheet_input error'
                })

            self.instagram_user_info = instagram_user_info

        if page_photo:
            if page_photo.size > 310000:
                self.add_error('page_photo', 'Размер изображения не должен превышать 300кб')
        if not popup_button_url.startswith('http://') and not popup_button_url.startswith('https://'):
            if not popup_button_url.startswith('tg:'):
                self.add_error('popup_button_url', 'Ссылка должна начинать с "http://", "https://" или с "tg://"')
                self.fields['popup_button_url'].widget.attrs.update({
                    'class': 'sheet_input error'
                })
        if not slug.isascii():
            self.add_error('slug', 'Ссылка должна содержать только английские символы')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        if not models.InstagramSubscribePage.is_slug_unique(slug):
            self.add_error('slug', 'Страница с такой ссылкой уже существует')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        return self.is_bound and not self.errors

    class Meta:
        model = models.InstagramSubscribePage
        exclude = [
            'user', 'group',
            'is_active', 'created'
        ]
        widgets = {
            'page_name': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Страница №1'
            }),
            'domain': forms.HiddenInput(),
            'slug': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Ссылка на страницу',
                'id': 'id_slug_create'
            }),
            'page_photo': forms.FileInput(attrs={
                'class': 'input__hidden',
                'id': 'photo',
            }),
            'bg_color': forms.HiddenInput(),
            'presubscribe_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст перед подпиской',
                'data-id': 'prew_sub'
            }),
            'precheck_subscribe_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст перед проверкой',
                'data-id': 'prew_ex'
            }),

            'title': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите заголовок страницы',
                'data-id': 'promo_title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите описание',
                'data-id': 'promo_text'
            }),
            'facebook_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'tiktok_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'vk_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'yandex_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID метрики'
            }),
            'roistat_id': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID Roistat'
            }),

            'button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст на кнопке',
                'data-id': 'promo_btn'
            }),

            'is_timer_active': forms.HiddenInput(),
            'timer_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'data-id': 'timer_text'
            }),
            'timer_time': forms.NumberInput(attrs={
                'class': 'sheet_input',
                'min': '0',
                'max': '3600',
                'data-id': 'timer'
            }),

            'instagram_username': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите логин',
                'data-id': 'user_name'
            }),
            'instagram_avatar': forms.FileInput(attrs={
                'class': 'input__hidden',
                'id': 'ava'
            }),

            'subscribe_button': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'subscribe_btn'
            }),
            'already_subscribed_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'yes_subscribe'
            }),
            'subscribed_button': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'signet_btn'
            }),
            'not_yet_subscribed': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'not_sibscribe'
            }),
            'search_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'search_text'
            }),
            'success_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'success_text'
            }),
            'error_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'error_text'
            }),

            'popup_title': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите заголовок',
                'data-id': 'hit_title'
            }),
            'popup_text': forms.Textarea(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите описание',
                'data-id': 'hit_text'
            }),
            'popup_button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст на кнопке',
                'data-id': 'hit_button'
            }),
            'popup_button_url': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ссылку',
                'data-id': 'hit_url'
            }),
            'single_page': forms.HiddenInput(),
            'show_subscribers': forms.HiddenInput(),
        }


class SubscribePageUpdateForm(forms.ModelForm):
    def is_valid(self):
        slug = self.data.get('slug').lower()
        popup_button_url = self.data.get('popup_button_url')
        page_photo = self.files.get('page_photo')

        if page_photo:
            if page_photo.size > 310000:
                self.add_error('page_photo', 'Размер изображения не должен превышать 300кб')
        if not popup_button_url.startswith('http://') and not popup_button_url.startswith('https://'):
            if not popup_button_url.startswith('tg:'):
                self.add_error('popup_button_url', 'Ссылка должна начинать с "http://", "https://" или с "tg://"')
                self.fields['popup_button_url'].widget.attrs.update({
                    'class': 'sheet_input error'
                })
        if not slug.isascii():
            self.add_error('slug', 'Ссылка должна содержать только английские символы')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        return self.is_bound and not self.errors

    class Meta:
        model = models.InstagramSubscribePage
        exclude = [
            'user', 'group',
            'is_active', 'created',
            'views', 'subscribed',
            'instagram_name', 'instagram_username'
        ]
        widgets = {
            'page_name': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Страница №1'
            }),
            'domain': forms.HiddenInput(),
            'slug': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Ссылка на страницу',
            }),
            'page_photo': forms.FileInput(attrs={
                'class': 'input__hidden',
                'id': 'photo',
            }),
            'bg_color': forms.HiddenInput(),
            'presubscribe_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст перед подпиской',
                'data-id': 'prew_sub'
            }),
            'precheck_subscribe_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст перед проверкой',
                'data-id': 'prew_ex'
            }),

            'title': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите заголовок страницы',
                'data-id': 'promo_title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите описание',
                'data-id': 'promo_text'
            }),
            'facebook_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'tiktok_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'vk_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'yandex_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID метрики'
            }),
            'roistat_id': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID Roistat'
            }),

            'button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст на кнопке',
                'data-id': 'promo_btn'
            }),

            'is_timer_active': forms.HiddenInput(),
            'timer_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'data-id': 'timer_text'
            }),
            'timer_time': forms.NumberInput(attrs={
                'class': 'sheet_input',
                'min': '0',
                'max': '3600',
                'data-id': 'timer'
            }),

            'instagram_avatar': forms.FileInput(attrs={
                'class': 'input__hidden',
                'id': 'ava'
            }),

            'subscribe_button': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'subscribe_btn'
            }),
            'already_subscribed_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'yes_subscribe'
            }),
            'subscribed_button': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'signet_btn'
            }),
            'not_yet_subscribed': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'not_sibscribe'
            }),
            'search_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'search_text'
            }),
            'success_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'success_text'
            }),
            'error_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст',
                'data-id': 'error_text'
            }),

            'popup_title': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите заголовок',
                'data-id': 'hit_title'
            }),
            'popup_text': forms.Textarea(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите описание',
                'data-id': 'hit_text'
            }),
            'popup_button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст на кнопке',
                'data-id': 'hit_button'
            }),
            'popup_button_url': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ссылку',
                'data-id': 'hit_url'
            }),
            'single_page': forms.HiddenInput(),
            'show_subscribers': forms.HiddenInput(),
        }


class SubscribePageDuplicateForm(forms.ModelForm):
    def is_valid(self, user=None):
        slug = self.data.get('slug').lower()

        if not slug.isascii():
            self.add_error('slug', 'Ссылка должна содержать только английский символы')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        if not models.InstagramSubscribePage.is_slug_unique(slug):
            self.add_error('slug', 'Страница с такой ссылкой уже существует')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })

        
        return self.is_bound and not self.errors

    class Meta:
        model = models.InstagramSubscribePage
        fields = [
            'page_name', 'slug', 'domain', 'instagram_username', 'instagram_avatar'
        ]
        labels = {
            'title': 'Заголовок страницы'
        }
        widgets = {
            'page_name': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Страница №1'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Ссылка на страницу'
            }),
            'instagram_username': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введи свой ник в инстаграм'
            }),
            'instagram_avatar': forms.FileInput(attrs={
                'class': 'input__hidden',
                'id': 'ava'
            })
        }


class InstagramLoginForm(forms.Form):
    instagram_username = forms.CharField(label=_('Login'), max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'subscript_input',
        'placeholder': 'Введи свой @ник в инстаграм',
        'autocomplete': 'off'
    }))


class DomainCreateForm(forms.ModelForm):

    def is_valid(self, user):
        domain = self.data.get('domain').replace('http://', '').replace('https://', '').replace('/', '').strip()
        if not domain:
            self.errors['domain'] = 'Введите домен'
            self.fields['domain'].widget.attrs.update({
                'class': 'sheet_input error',
            })
        else:
            exists = models.Domain.objects.filter(domain=domain, user=user, for_delete=False)
            if exists:
                self.add_error('domain', 'У вас уже есть данный домен')
                self.fields['domain'].widget.attrs.update({
                    'class': 'sheet_input error'
                })
            forbidden_characters = set(re.findall('[^\daA-zZаА-яЯ\.-]', domain))

            if forbidden_characters:
                forbidden_characters = list(map(lambda x: f'"{x}"', forbidden_characters))
                self.add_error('domain', 'Домен содержит запрещённые символы:')
                self.add_error('domain', ', '.join(forbidden_characters))

        if not self.errors:
            try:
                ip = socket.gethostbyname(domain)
            except Exception as e:
                ip = None
                loggerDomain.warning(
                    f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} task_domain_add_get_ip: {domain}` -- {e}\n')
            if ip != '62.109.7.205':
                self.add_error('domain', 'Домен еще не привязан к нашему IP адресу')
        return super().is_valid()

    class Meta:
        model = models.Domain
        fields = ['domain']
        widgets = {
            'domain': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'domain.com',
                'id': 'domain'
            })
        }


# vk folders
class VKGroupCreateForm(forms.ModelForm):
    class Meta:
        model = models.VKGroupOfSubscribePage
        fields = ['name']

    def is_valid(self):
        name = self.data.get('name')
        forbidden_characters = set(re.findall('[^\daA-zZаА-яЯ\.-]', name))

        if forbidden_characters:
            forbidden_characters = list(
                map(lambda x: f'"{x}"', forbidden_characters))
            self.add_error('name', 'Название содержит запрещённые символы:')
            self.add_error('name', ', '.join(forbidden_characters))
        return self.is_bound and not self.errors


class VKGroupRenameForm(forms.ModelForm):
    class Meta:
        model = models.VKGroupOfSubscribePage
        fields = ['name']


class VKAddToFolderForm(forms.ModelForm):
    def is_valid(self, user):
        slug = self.data.get('slug')

        exist = models.VKSubscribePage.objects.filter(user=user, slug=slug)
        if not exist:
            self.add_error('slug', 'Не удалось найти страницу')

        return super().is_valid()

    class Meta:
        model = models.VKSubscribePage
        fields = ['slug', 'group']
        widgets = {
            'slug': forms.HiddenInput(attrs={
                'class': 'AddToFolder',
                'id': 'page_slug'
            }),
            'group': forms.HiddenInput(attrs={
                'class': 'AddToFolder',
                'id': 'folder_id'
            }),
        }


# vk subscribe pages
class VKSubscribePageCreateForm(forms.ModelForm):
    def is_valid(self):
        slug = self.data.get('slug').lower()
        success_button_url = self.data.get('success_button_url')
        page_photo = self.files.get('page_photo')

        if page_photo:
            if page_photo.size > 310000:
                self.add_error('page_photo', 'Размер изображения не должен превышать 300кб')
        if not success_button_url.startswith('http://') and not success_button_url.startswith('https://'):
            if not success_button_url.startswith('tg:'):
                self.add_error('success_button_url', 'Ссылка должна начинать с "http://", "https://" или с "tg://"')
                self.fields['success_button_url'].widget.attrs.update({
                    'class': 'sheet_input error'
                })
        if not slug.isascii():
            self.add_error('slug', 'Ссылка должна содержать только английские символы')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        if not models.VKSubscribePage.is_slug_unique(slug):
            self.add_error('slug', 'Страница с такой ссылкой уже существует')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        return self.is_bound and not self.errors

    class Meta:
        model = models.VKSubscribePage
        exclude = [
            'user', 'group',
            'is_active', 'created'
        ]
        widgets = {
            'page_name': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Страница №1'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Ссылка на страницу',
                'id': 'id_slug_create'
            }),
            'vk_group_id': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID группы'
            }),
            'type_group_id': forms.HiddenInput(),
            'page_photo': forms.FileInput(attrs={
                'class': 'input__hidden',
                'id': 'photo',
            }),
            'bg_color': forms.HiddenInput(),

            'title': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите заголовок страницы',
                'data-id': 'promo_title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите описание',
                'data-id': 'promo_text'
            }),
            'button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст на кнопке',
                'data-id': 'promo_btn'
            }),

            'facebook_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'tiktok_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'vk_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'yandex_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID метрики'
            }),
            'roistat_id': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID Roistat'
            }),

            'is_timer_active': forms.HiddenInput(),
            'timer_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'data-id': 'timer_text'
            }),
            'timer_time': forms.NumberInput(attrs={
                'class': 'sheet_input',
                'min': '0',
                'max': '3600',
                'data-id': 'timer'
            }),

            'success_title': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите заголовок',
                'data-id': 'hit_title'
            }),
            'success_text': forms.Textarea(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите описание',
                'data-id': 'hit_text'
            }),
            'success_button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст на кнопке',
                'data-id': 'hit_button'
            }),
            'success_button_url': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ссылку',
                'data-id': 'hit_url'
            }),
        }


class VKSubscribePageUpdateForm(forms.ModelForm):
    def is_valid(self):
        slug = self.data.get('slug').lower()
        success_button_url = self.data.get('success_button_url')
        page_photo = self.files.get('page_photo')

        if page_photo:
            if page_photo.size > 310000:
                self.add_error('page_photo', 'Размер изображения не должен превышать 300кб')
        if not success_button_url.startswith('http://') and not success_button_url.startswith('https://'):
            if not success_button_url.startswith('tg:'):
                self.add_error('success_button_url', 'Ссылка должна начинать с "http://", "https://" или с "tg://"')
                self.fields['success_button_url'].widget.attrs.update({
                    'class': 'sheet_input error'
                })
        if not slug.isascii():
            self.add_error('slug', 'Ссылка должна содержать только английские символы')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        return self.is_bound and not self.errors

    def clean_vk_group_id(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.vk_group_id
        else:
            return self.cleaned_data['vk_group_id']

    def clean_type_group_id(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.type_group_id
        else:
            return self.cleaned_data['type_group_id']

    class Meta:
        model = models.VKSubscribePage
        exclude = [
            'user', 'group',
            'is_active', 'created',
            'views', 'subscribed'
        ]
        widgets = {
            'page_name': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Страница №1'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Ссылка на страницу',
            }),
            'vk_group_id': forms.TextInput(attrs={
                'class': 'sheet_input rea',
                'placeholder': 'Введите ID группы',
                'readonly': 'readonly'
            }),
            'type_group_id': forms.HiddenInput(),
            'page_photo': forms.FileInput(attrs={
                'class': 'input__hidden',
                'id': 'photo',
            }),
            'bg_color': forms.HiddenInput(),

            'title': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите заголовок страницы',
                'data-id': 'promo_title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите описание',
                'data-id': 'promo_text'
            }),
            'button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст на кнопке',
                'data-id': 'promo_btn'
            }),

            'facebook_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'tiktok_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'vk_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID пикселя'
            }),
            'yandex_pixel': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID метрики'
            }),
            'roistat_id': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID Roistat'
            }),

            'is_timer_active': forms.HiddenInput(),
            'timer_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'data-id': 'timer_text'
            }),
            'timer_time': forms.NumberInput(attrs={
                'class': 'sheet_input',
                'min': '0',
                'max': '3600',
                'data-id': 'timer'
            }),

            'success_title': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите заголовок',
                'data-id': 'hit_title'
            }),
            'success_text': forms.Textarea(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите описание',
                'data-id': 'hit_text'
            }),
            'success_button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст на кнопке',
                'data-id': 'hit_button'
            }),
            'success_button_url': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ссылку',
                'data-id': 'hit_url'
            }),
        }


class VKSubscribePageDuplicateForm(forms.ModelForm):
    def is_valid(self, user=None):
        slug = self.data.get('slug').lower()

        if not slug.isascii():
            self.add_error('slug', 'Ссылка должна содержать только английский символы')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        if not models.VKSubscribePage.is_slug_unique(slug):
            self.add_error('slug', 'Страница с такой ссылкой уже существует')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'.casefold()
            })

        return self.is_bound and not self.errors

    class Meta:
        model = models.VKSubscribePage
        fields = [
            'page_name', 'slug', 'vk_group_id', 'type_group_id'
        ]
        labels = {
            'title': 'Заголовок страницы'
        }
        widgets = {
            'page_name': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Страница №1'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Ссылка на страницу'
            }),
            'vk_group_id': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите ID группы'
            }),
            'type_group_id': forms.HiddenInput()
        }
