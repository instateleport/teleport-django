import re

from django import forms

from .models import TelegramSubscribePage
from .models import TelegramGroupOfSubscribePage

class TGSubscribePageDuplicateForm(forms.ModelForm):
    def is_valid(self, user=None):
        slug = self.data.get('slug').lower()

        if not slug.isascii():
            self.add_error('slug', 'Ссылка должна содержать только английский символы')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        if not TelegramSubscribePage.is_slug_unique(slug):
            self.add_error('slug', 'Страница с такой ссылкой уже существует')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })

        
        return self.is_bound and not self.errors

    class Meta:
        model = TelegramSubscribePage
        fields = [
            'page_name',
            'slug',
            'domain'
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
        }


class TGGroupRenameForm(forms.ModelForm):
    class Meta:
        model = TelegramGroupOfSubscribePage
        fields = ['name']


class TGGroupCreateForm(forms.ModelForm):
    class Meta:
        model = TelegramGroupOfSubscribePage
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


class AddToTelegramFolderForm(forms.ModelForm):
    def is_valid(self, user):
        slug = self.data.get('slug')

        exist = TelegramSubscribePage.objects.filter(user=user, slug=slug)
        if not exist:
            self.add_error('slug', 'Не удалось найти страницу')

        return super().is_valid()

    class Meta:
        model = TelegramSubscribePage
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


class TGSubscribePageUpdateForm(forms.ModelForm):
    def is_valid(self):
        slug = self.data.get('slug').lower()
        page_photo = self.files.get('page_photo')

        if page_photo:
            if page_photo.size > 310000:
                self.add_error('page_photo', 'Размер изображения не должен превышать 300кб')
        if not slug.isascii():
            self.add_error('slug', 'Ссылка должна содержать только английские символы')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        return self.is_bound and not self.errors

    class Meta:
        model = TelegramSubscribePage
        exclude = [
            'user', 
            'group',
            'is_active',
            'instagram_username',
            'created',
            'page_hash'
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
            'message_after_getting_present': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'сообщения при получении подарка (бот)',
            }),
            'button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'текст на кнопке (бот)',
            }),
            'button_url': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'ссылка кнопки (бот)',
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
            'popup_button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст на кнопке',
                'data-id': 'hit_button'
            }),
        }

 

class TGSubscribePageCreateForm(forms.ModelForm):
    def is_valid(self):
        slug = self.data.get('slug').lower()
        page_photo = self.files.get('page_photo')

        if page_photo:
            if page_photo.size > 310000:
                self.add_error('page_photo', 'Размер изображения не должен превышать 300кб')
        if not slug.isascii():
            self.add_error('slug', 'Ссылка должна содержать только английские символы')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        if not TelegramSubscribePage.is_slug_unique(slug):
            self.add_error('slug', 'Страница с такой ссылкой уже существует')
            self.fields['slug'].widget.attrs.update({
                'class': 'sheet_input error'
            })
        return self.is_bound and not self.errors

    class Meta:
        model = TelegramSubscribePage
        exclude = [
            'user',
            'group',
            'is_active',
            'created',
            'page_hash',
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
            'message_after_getting_present': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'сообщения при получении подарка (бот)',
            }),
            'button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'текст на кнопке (бот)',
            }),
            'button_url': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'ссылка кнопки (бот)',
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
            'popup_button_text': forms.TextInput(attrs={
                'class': 'sheet_input',
                'placeholder': 'Введите текст на кнопке',
                'data-id': 'hit_button'
            }),
        }
