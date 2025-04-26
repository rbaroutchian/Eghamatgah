from django.db import models
from eghamatgah.models import Eghamatgah
from user_account.models import User
# Create your models here.


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    eghamat = models.ForeignKey(Eghamatgah, on_delete=models.CASCADE, verbose_name='اقامتگاه')
    check_in = models.DateField(verbose_name='تاریخ ورود', null=True, blank=True)
    check_out = models.DateField(verbose_name='تاریخ خروج', null=True, blank=True)
    persons = models.PositiveIntegerField(verbose_name='تعداد نفرات')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'در انتظار'), ('confirmed', 'تایید شده'), ('cancelled', 'لغو شده')], default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.eghamat} ({self.check_in} to {self.check_out})"

    class Meta:
        verbose_name = 'رزرو'
        verbose_name_plural = 'همه رزروها'
