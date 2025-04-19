from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('register/', views.Register.as_view(), name='register_page'),
    path('logout/', views.user_logout, name='logout_page'),
    path('verify-code/', views.VerifyCodeView.as_view(), name='verify_code_page'),
    path('user-profile/', views.EditUserProfilePage.as_view(), name='profile'),

]
