"""
JudgeLoom — Core Middleware
==============================

Custom middleware classes for cross-cutting concerns.

Classes:
    TimezoneMiddleware: Activates user-preferred timezone per request.
    RequestMetricsMiddleware: Logs request duration for monitoring.
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

from django.utils import timezone as dj_timezone

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class TimezoneMiddleware:
    """Activate the user's preferred timezone for each request.

    Reads ``timezone`` from the user profile (if authenticated) and
    calls ``django.utils.timezone.activate()`` so that template
    rendering and date formatting use the correct local time.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request with timezone activation.

        Args:
            request: The incoming HTTP request.

        Returns:
            The HTTP response from downstream middleware/views.
        """
        if hasattr(request, "user") and request.user.is_authenticated:
            user_tz = getattr(request.user, "timezone", None)
            if user_tz:
                try:
                    dj_timezone.activate(user_tz)
                except Exception:  # noqa: BLE001 — invalid tz should not crash
                    dj_timezone.deactivate()
            else:
                dj_timezone.deactivate()
        else:
            dj_timezone.deactivate()

        return self.get_response(request)


class RequestMetricsMiddleware:
    """Log request processing time for basic performance monitoring.

    Emits an INFO log line with the method, path, status code, and
    elapsed milliseconds for every request. In production this feeds
    into structured logging / Sentry performance tracing.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Measure and log request duration.

        Args:
            request: The incoming HTTP request.

        Returns:
            The HTTP response from downstream middleware/views.
        """
        start = time.monotonic()
        response = self.get_response(request)
        elapsed_ms = (time.monotonic() - start) * 1000

        # Skip static file requests to reduce log noise
        if not request.path.startswith(("/static/", "/media/", "/__debug__/")):
            logger.info(
                "%s %s → %d (%.1fms)",
                request.method,
                request.path,
                response.status_code,
                elapsed_ms,
            )

        return response
