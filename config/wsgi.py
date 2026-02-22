"""
JudgeLoom — WSGI Configuration
================================

Exposes the WSGI application for traditional HTTP request handling.

Deployment::

    gunicorn config.wsgi:application --workers 4
"""

from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

application = get_wsgi_application()
