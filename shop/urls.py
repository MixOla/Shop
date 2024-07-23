from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('basket/', include('basket.urls', namespace='basket')),
    path('/', include('store.urls', namespace='store'))
]
