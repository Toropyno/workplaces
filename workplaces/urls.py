from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('a_places.api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
