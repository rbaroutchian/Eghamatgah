from django.contrib import admin
from . import models
# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ('Fullname', 'Email', 'is_read_admin')
    list_editable = ('is_read_admin',)


admin.site.register(models.Contact, ContactAdmin),

