from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm, SetPasswordForm, UserChangeForm, AuthenticationForm, UsernameField,
    PasswordResetForm
)
from django.utils.translation import gettext_lazy as _
from django.forms import EmailInput
from django import forms

from . import models


class CustomUserAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'class': 'input',
        'autofocus': True,
        'placeholder': 'Введите логин'
    }))
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'input',
            'placeholder': 'Введите пароль',
            'id': 'inp_1'
        })
    )


class CustomUsernameField(UsernameField):
    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'off',
            'class': 'login_input',
            'placeholder': 'Введите логин',
        }


class CustomUserCreationForm(UserCreationForm):
    error_css_class = 'error'
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'off',
            'class': 'input',
            'placeholder': 'Введите пароль',
            'id': 'inp_1'
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'input',
            'placeholder': 'Подтвердите пароль',
            'id': 'inp_2'
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def is_valid(self):
        username = self.data['username']
        forbidden_characters = ''
        for forbidden_character in ['/', ':', ';', ',', '|', '+', '=', '@']:
            if forbidden_character in username:
                forbidden_characters += f'"{forbidden_character}", '

        if forbidden_characters:
            forbidden_characters = forbidden_characters[:-2]
            self.add_error('username', 'Логин содержит запрещённые символы:')
            self.add_error('username', forbidden_characters)

        if len(username) < 4:
            self.add_error('username', 'Логин должен быть длиннее 3 символов')
        if not str(username).isascii():
            self.add_error('username', 'Логин должен содержать только английские буквы')
        return self.is_bound and not self.errors

    class Meta:
        model = models.CustomUser
        fields = ['username', 'email', 'phone']
        field_classes = {'username': CustomUsernameField}
        widgets = {
            'email': EmailInput(attrs={
                'placeholder': 'Введите ваш email',
                'required': True,
                'class': 'input'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Введите ваш номер',
                'required': False
            })
        }


class CustomUserChangeForm(UserChangeForm):
    user_change_form_name = forms.Field(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                'name': 'user_change_form',
                'required': False
            }
        )
    )

    class Meta:
        model = models.CustomUser
        fields = [
            # 'avatar',
            'email'
        ]
        widgets = {
            # 'avatar': forms.FileInput(attrs={
            #     'id': 'ava',
            #     'class': 'input__hidden',
            #     'required': False
            # }),
            'email': forms.EmailInput(attrs={
                'class': 'input'
            }),
        }


class CustomUserPasswordChangeForm(PasswordChangeForm):
    password_change_form_name = forms.Field(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                'name': 'password_change_form',
            }
        )
    )
    old_password = forms.CharField(
        label='Старый пароль',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'autofocus': True,
                'placeholder': 'Введите старый пароль'
            }
        )
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Введите новый пароль'
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'placeholder': 'Повторите новый пароль'
            }
        )
    )

    class Meta:
        model = models.CustomUser


class CustomUserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'login_input',
                'placeholder': 'Введите новый пароль',
                'id': 'inp_1'
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'login_input',
                'placeholder': 'Подтвердите новый пароль',
                'id': 'inp_2'
            }
        )
    )

    class Meta:
        model = models.CustomUser


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(max_length=100, required=True, widget=forms.EmailInput(
        attrs={
            'autocomplete': 'email',
            'class': 'reestab_input',
            'placeholder': 'Введите свою почту'
        }
    ))

    def is_valid(self):
        email = self.data['email']
        if not models.CustomUser.objects.filter(email=email):
            self.add_error('email', 'Почта не найдена')
        return self.is_bound and not self.errors
