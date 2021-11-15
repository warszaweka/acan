from django.urls import path

from .views import csrf, media

app_name = 'acan'
urlpatterns = [
    path('csrf', csrf, name='csrf'),
    path('media/<path:relative_path>', media, name='media'),
]
