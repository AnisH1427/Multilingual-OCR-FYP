from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .views import tensorboard

router = DefaultRouter()
router.register(r'document', views.DocumentViewSet)

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('api/',include(router.urls)),
    path('api/predict/',views.PredictView.as_view(),name='predict'),
    path('user-update/', views.UserUpdateView.as_view(), name='user_update'),
    path('delete-user/<str:username>/', views.UserDeleteView.as_view(),name='delete-user'),
    path('tensorboard/', tensorboard, name='tensorboard'),
    path('guide/', views.guide, name='guide'),
]
