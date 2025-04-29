from django import forms
from .models import Seller


class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['company_name', 'phone']
