from django import forms
from .models import Eghamatgah, EghamatComment, Seller


class EghamatForm(forms.ModelForm):
    class Meta:
        model = Eghamatgah
        fields = '__all__'

    def clean_description(self):
        description = self.cleaned_data['description']
        return description.encode('utf-8').decode('utf-8')

class EghamatCommentForm(forms.ModelForm):
    class Meta:
        model = EghamatComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'نظر خود را بنویسید'}),
        }


class EghamatCommentFormAdmin(forms.ModelForm):
    class Meta:
        model = EghamatComment
        fields = ['eghamat', 'user', 'text']




class EghamatSearchForm(forms.Form):
    destination = forms.CharField(label="شهر مقصد", max_length=50, required=False)
    check_in = forms.DateField(label="تاریخ ورود", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    check_out = forms.DateField(label="تاریخ خروج", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    persons = forms.IntegerField(label="تعداد نفرات", min_value=1, required=False)
