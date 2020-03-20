from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('my_site.urls')),
    path('', include('apps.psw.urls')),
    path('admin/', admin.site.urls),
]
