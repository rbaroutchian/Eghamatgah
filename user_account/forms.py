from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={
            'class': 'form-control rounded-pill py-2 px-3 shadow-sm',
            'placeholder': 'نام کاربری خود را وارد کنید',
            'style': 'font-size: 15px;'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    Password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control rounded-pill py-2 px-3 shadow-sm',
            'placeholder': 'رمز عبور خود را وارد کنید',
            'style': 'font-size: 15px;'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور'
        }),
        validators=[validators.MaxLengthValidator(100)]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'user_number', 'password']
        labels = {
            'username': 'نام کاربری',
            'email': 'ایمیل',
            'user_number': 'شماره تماس',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کاربری'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل'
            }),
            'user_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره تماس'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

