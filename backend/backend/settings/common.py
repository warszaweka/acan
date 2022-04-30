from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
INSTALLED_APPS = [
    'acan.apps.AcanConfig',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'corsheaders',
    'django_simple_coupons',
]
LANGUAGE_CODE = 'uk'
LANGUAGES = [
    ('uk', 'Ukrainian'),
    ('ru', 'Russian'),
]
MEDIA_ROOT = BASE_DIR / 'media'
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'acan.middleware.LanguageMiddleware',
]
ROOT_URLCONF = 'backend.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
USE_I18N = True
AUTH_USER_MODEL = 'acan.User'
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
STATIC_ROOT = BASE_DIR / 'static'
GRAPHENE = {
    'SCHEMA': 'backend.schema.schema',
}
CORS_ALLOW_CREDENTIALS = True
DSC_COUPON_CODE_LENGTH = 16
