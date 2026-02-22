from __future__ import annotations

from django.apps import AppConfig


class SubmissionsConfig(AppConfig):
    """Application configuration for submission lifecycle management."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.submissions"
    label = "submissions"
    verbose_name = "Submissions"
