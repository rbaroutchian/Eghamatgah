from django.db import models
from user_account.models import User
# Create your models here.


class Seller(models.Model):
    name = models.CharField(max_length=300,null=True, verbose_name='نام و نام خانوداگی')
    company_name = models.CharField(max_length=20, null=True, verbose_name='نام شرکت/کمپانی')
    phone_number = models.CharField(max_length=50,null=True, verbose_name='تلفن همراه')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'فروشنده'
        verbose_name_plural = 'فروشندگان'
