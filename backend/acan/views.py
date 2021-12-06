from json import loads
from base64 import b64encode, b64decode
from hashlib import sha1
from re import fullmatch

from acan.models import Course, Lesson
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import FileResponse, HttpResponseNotFound, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


def csrf(request):
    return JsonResponse({
        'token': get_token(request),
    })


def media(request, relative_path):
    allowed = False
    if Course.objects.filter(image=relative_path).exists():
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
            sha1(settings.LIQPAY_PRIVATE_KEY + data +
                 settings.LIQPAY_PRIVATE_KEY).digest()
    ).decode('ascii') == request.POST['signature']:
        import sys  # DEBUG
        print(loads(b64decode(data).decode('utf-8')), file=sys.stderr)  # DEBUG
    return HttpResponse()
