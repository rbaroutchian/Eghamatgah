from django.contrib import admin
from . import models
# Register your models here.
class SellerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'is_active']
    list_editable = ['is_active']
admin.site.register(models.Seller, SellerAdmin)