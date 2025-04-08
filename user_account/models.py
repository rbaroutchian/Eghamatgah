from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    user_number = models.CharField(max_length=50, null=True, verbose_name='شماره تماس')
    avatar = models.ImageField(upload_to='media', default='', null=True, verbose_name='آواتار')
    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'