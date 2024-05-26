from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from authentication.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('app/', include('app.urls')),
    #  path('api/auth/logout/', logout_view, name='logout_view'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
