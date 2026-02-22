from __future__ import annotations

from django.apps import AppConfig


class ContestsConfig(AppConfig):
    """Application configuration for contests domain."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.contests"
    verbose_name = "Contests"
