from django.urls import path, include
from dj_rest_auth.views import LoginView, LogoutView,UserDetailsView
from dj_rest_auth.registration.views import RegisterView
from . import views
from .views import CustomRegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/auth/login/', LoginView.as_view(), name='rest_login'),
    path('api/auth/logout/', LogoutView.as_view(), name='rest_logout'),
    path('api/auth/user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('api/auth/register/', CustomRegisterView.as_view(), name='api/auth/rest_register'),
    path('', views.home, name='home'),
    path('login/', views.loginpage, name='loginpage'),
    path('register/',views.register,name='register'),
    path('login_with_token/', views.login_with_token, name='login_with_token'),   
    path('accounts/', include('allauth.urls')), 
]
