from base64 import b64decode, b64encode
from hashlib import sha1
from json import loads
from re import fullmatch

from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import (FileResponse, HttpResponse, HttpResponseNotFound,
                         JsonResponse)
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from acan.models import Course, Lesson, Order


def csrf(request):
    return JsonResponse({
        'token': get_token(request),
    })


def media(request, relative_path):
    allowed = False
    if relative_path.startswith('article_images/'):
        allowed = True
    elif Course.objects.filter(image=relative_path).exists():
        allowed = True
    else:
        match = fullmatch(r'lesson_(\d*)_\d*\.ts', relative_path)
        if match:
            video_path = f'lesson_{match.group(1)}_.m3u8'
        else:
            video_path = relative_path
        if get_object_or_404(Lesson,
                             Q(addon=relative_path) | Q(video=video_path),
                             course__published=True).course.purchased(
                                 request.user):
            allowed = True
    if allowed and default_storage.exists(relative_path):
        return FileResponse(default_storage.open(relative_path))
    return HttpResponseNotFound()


@csrf_exempt
def payment(request):
    data = request.POST['data']
    if b64encode(
            sha1((f'{settings.LIQPAY_PRIVATE_KEY}{data}' +
                  settings.LIQPAY_PRIVATE_KEY).encode('utf-8')).digest()
    ).decode('ascii') == request.POST['signature']:
        clear_data = loads(b64decode(data).decode('utf-8'))
        if clear_data['status'] == 'success':
            order = Order.objects.get(pk=clear_data['order_id'])
            order.payed = True
            order.save()
    return HttpResponse()
