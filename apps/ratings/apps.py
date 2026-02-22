from __future__ import annotations

from django.apps import AppConfig


class RatingsConfig(AppConfig):
    """Application configuration for ratings domain."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ratings"
    verbose_name = "Ratings"
