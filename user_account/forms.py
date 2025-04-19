from django import forms
from django.core.exceptions import ValidationError
from django.core import validators
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام کاربری'
        }),
        validators=[
            validators.MaxLengthValidator(100),

        ]
    )
    Password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور'

        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_number', 'password']


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

