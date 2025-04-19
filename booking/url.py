from django.urls import path
from eghamatgah.views import EghamatDetail

urlpatterns = [
    path('<int:pk>/', EghamatDetail.as_view(), name='booking'),
]