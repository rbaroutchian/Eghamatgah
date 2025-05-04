from django.urls import path
from . import views

urlpatterns = [
    path('eghamat_list/',views.EghamatList.as_view(), name='eghamat_list'),
    path('eghamat_detail/<int:pk>', views.EghamatDetail.as_view(), name='eghamat_detail'),
    path('<int:pk>/calculate_price/', views.calculate_price, name='calculate_price'),
    path('add-favorite/', views.add_to_fav, name='add_favorite'),
    path('my-favorites/', views.fav_list, name='my_favorites'),

]
