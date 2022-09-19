from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    #path('login/', include('main.urls')),
    path('docs/', include('docs.urls')),
    path('directory/', include('directory.urls')),
    path('reports/', include('reports.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/token', obtain_auth_token, name='token'),
    #path('auth/', include('djoser.urls.jwt')),
    #path('/auth-token/', include('djoser.urls.authtoken')),
    #path('/api-auth/', include('rest_framework.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
