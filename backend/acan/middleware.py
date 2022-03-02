from django.conf import settings


class LanguageMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        language = getattr(request, 'acan_set_language_cookie', None)
        if language:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
