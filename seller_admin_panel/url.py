from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='admin_home'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('eghamat_list_dashboard/', views.EghamatgahList.as_view(), name='eghamat_list_dashboard'),
    path('eghamat_add/', views.Eghamatgah_add.as_view(), name='add_eghamat'),
    path('eghamat_category/', views.Eghamatgah_Category_admin.as_view(), name='category_eghamat'),
    path('eghamat_update/<pk>', views.Eghamatgah_Detail.as_view(), name='update_eghamat'),
    path('eghamat_delete/<int:pk>/', views.Eghamatgah_Delete.as_view(), name='delete_eghamat'),
    path('eghamat_category_delete/<int:pk>/', views.Category_Delete.as_view(), name='delete_eghamat_category'),


]