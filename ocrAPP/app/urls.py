from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'document', views.DocumentViewSet)

urlpatterns = [
    path('home/', views.home, name='home'),
    path('api/',include(router.urls)),
    path('api/predict/',views.PredictView.as_view(),name='predict'),
]
