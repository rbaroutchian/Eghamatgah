from django.urls import path
from . import views

urlpatterns = [
    path('eghamat_list/',views.EghamatList.as_view(), name='eghamat_list'),
    path('eghamat_detail/<int:pk>', views.EghamatDetail.as_view(), name='eghamat_detail'),
    path('<int:pk>/calculate_price/', views.calculate_price, name='calculate_price'),

]
