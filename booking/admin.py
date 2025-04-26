from django.contrib import admin
from . import models
from .models import Booking
# Register your models here.


class admin_booking_list(admin.ModelAdmin):
    list_display = ['user', 'eghamat']


admin.site.register(models.Booking, admin_booking_list)
