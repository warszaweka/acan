#!/usr/bin/env python
from os import environ
from wsgiref.handlers import CGIHandler

from django.core.wsgi import get_wsgi_application

environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
CGIHandler().run(get_wsgi_application())
