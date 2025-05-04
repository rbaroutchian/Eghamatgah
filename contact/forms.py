from django import forms
from .models import Contact


class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['Fullname', 'Email', 'Title', 'Phone', 'Message']
        widgets = {
            'Fullname': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'نام و نام خانوادگی',
            }),
            'Email': forms.EmailInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'ایمیل شما',
            }),
            'Title': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'موضوع پیام شما',
            }),
            'Phone': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'موبایل شما',
            }),
            'Message': forms.Textarea(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'پیام شما',
                'rows': 5,
                'id': 'cf-message'
            }),
        }
        labels = {
            'Fullname': 'نام و نام خانوادگی',
            'Email': 'ایمیل',
            'Title': 'موضوع',
            'Phone': 'تلفن همراه',
            'Message': 'پیام خود را بنویسید'
        }
        error_messages = {
            'Fullname': {
                'required': 'لطفاً نام و نام خانوادگی را وارد کنید',
            },
            'Email': {
                'required': 'لطفاً ایمیل خود را وارد کنید',
                'invalid': 'ایمیل معتبر نیست',
            },
            'Phone': {
                'required': 'لطفاً شماره تلفن را وارد کنید',
            },
        }