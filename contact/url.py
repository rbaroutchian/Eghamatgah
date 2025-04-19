from django.urls import path
from . import views

urlpatterns = [
    path('', views.contactView.as_view(), name="contact_page"),
]
