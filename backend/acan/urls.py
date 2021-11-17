from django.urls import path

from .views import csrf, media, payment

app_name = 'acan'
urlpatterns = [
    path('csrf', csrf, name='csrf'),
    path('media/<path:relative_path>', media, name='media'),
    path('payment', payment, name='payment'),
]
