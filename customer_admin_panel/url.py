from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_admin_panel, name='customer_admin_home'),
    path('user-profile', views.EditUserProfile.as_view(), name='user_profile')
    ]
