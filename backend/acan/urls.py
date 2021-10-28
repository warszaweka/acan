from django.urls import path

from .views import csrf

app_name = 'acan'
urlpatterns = [
    path('csrf', csrf, name='csrf'),
]
