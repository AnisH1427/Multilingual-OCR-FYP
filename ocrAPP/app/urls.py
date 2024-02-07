from django.urls import path
from .views import custom_register, custom_login

urlpatterns = [
    path('custom-register/', custom_register, name='custom-register'),
    path('custom-login/', custom_login, name='custom-login'),
    # Add other URLs as needed
]
