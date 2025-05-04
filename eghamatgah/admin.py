from django.contrib import admin
from .models import Eghamatgah, EghamatComment, Eghamatgah_Category, AvailableDate, Favorite
from . import models


class AvailableDateInline(admin.TabularInline):
    model = AvailableDate
    extra = 1


class admin_Eghamatgah_list(admin.ModelAdmin):
    inlines = [AvailableDateInline]
    list_display = ['title', 'seller', 'shahr']
    list_filter = ['seller', 'shahr']
    search_fields = ['title', 'seller', 'shahr']


admin.site.register(models.Eghamatgah, admin_Eghamatgah_list)
admin.site.register(EghamatComment)
admin.site.register(Eghamatgah_Category)
admin.site.register(AvailableDate)
admin.site.register(Favorite)

