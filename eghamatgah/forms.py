from django import forms
from .models import Eghamatgah


class EghaatForm(forms.ModelForm):
    class Meta:
        model = Eghamatgah
        fields = '__all__'
