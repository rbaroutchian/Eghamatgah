from django import forms
from .models import Booking, Eghamatgah
from eghamatgah.models import AvailableDate


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'persons']

    # فیلدهای تاریخ رو به طور داینامیک با تاریخ‌های قابل رزرو پر می‌کنیم
    def __init__(self, *args, **kwargs):
        eghamat = kwargs.pop('eghamat', None)  # این مدل اقامتگاه برای فیلتر کردن تاریخ‌ها میاد
        super().__init__(*args, **kwargs)

        if eghamat:
            # دریافت تاریخ‌های غیرقابل رزرو از مدل UnavailableDate
            unavailable_dates = eghamat.unavailable_dates.values_list('date', flat=True)

            # محدود کردن تاریخ‌ها برای فیلد تاریخ ورود و خروج
            self.fields['check_in'].widget = forms.SelectDateWidget(
                years=range(2025, 2030),
                empty_label=("انتخاب کنید", "انتخاب کنید", "انتخاب کنید"),
                attrs={'class': 'form-control', 'min': str(eghamat.created_at.date())}
            )
            self.fields['check_out'].widget = forms.SelectDateWidget(
                years=range(2025, 2030),
                empty_label=("انتخاب کنید", "انتخاب کنید", "انتخاب کنید"),
                attrs={'class': 'form-control', 'min': str(eghamat.created_at.date())}
            )

            # اعمال تاریخ‌های غیرقابل رزرو برای تاریخ خروج و ورود
            self.fields['check_in'].queryset = AvailableDate.objects.filter(
                eghamat=eghamat).exclude(date__in=unavailable_dates)

            self.fields['check_out'].queryset = AvailableDate.objects.filter(
                eghamat=eghamat).exclude(date__in=unavailable_dates)