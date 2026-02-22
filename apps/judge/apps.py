from __future__ import annotations

from django.apps import AppConfig


class JudgeConfig(AppConfig):
    """Application configuration for judge connectivity and runtimes."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.judge"
    label = "judge"
    verbose_name = "Judge"
