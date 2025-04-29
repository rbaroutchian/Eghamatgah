from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='admin_home'),
    path('sidebar/', views.sidebarview, name='sidebar'),
    path('eghamat_list_dashboard/', views.EghamatgahList.as_view(), name='eghamat_list_dashboard'),
    path('eghamat_add/', views.Eghamatgah_add.as_view(), name='add_eghamat'),
    path('eghamat_category/', views.Eghamatgah_Category_admin.as_view(), name='category_eghamat'),
    path('eghamat_update/<pk>', views.Eghamatgah_Detail.as_view(), name='update_eghamat'),
    path('eghamat_delete/<int:pk>/', views.Eghamatgah_Delete.as_view(), name='delete_eghamat'),
    path('eghamat_category_delete/<int:pk>/', views.Category_Delete.as_view(), name='delete_eghamat_category'),
    path('bookig_list/', views.booking_eghamat.as_view(), name='booking_list'),
    path('eghamat/comment_list/', views.EghamatCommentAdmin.as_view(), name='comment_list'),
    path('daramad/', views.daramad_view, name='daramad'),
    path('daramad/ajax/', views.daramad_ajax, name='daramad_ajax'),
    path('profile/seller_profile', views.EditSellerProfilePage.as_view(), name='seller_profile'),

]
