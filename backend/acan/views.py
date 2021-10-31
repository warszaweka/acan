from django.http import JsonResponse
from django.middleware.csrf import get_token


def csrf(request):
    return JsonResponse({
        'token': get_token(request),
    })
