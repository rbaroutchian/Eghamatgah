from django.db import models
from user_account.models import User



# Create your models here.


class Seller(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='seller', verbose_name='کاربر')
    company_name = models.CharField(max_length=255, verbose_name='نام کمپانی')
    phone = models.CharField(max_length=15, blank=True, verbose_name='شماره تماس')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین /غیر ادمین')

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'فروشنده'
        verbose_name_plural = 'فروشندگان'
