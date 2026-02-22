from __future__ import annotations

from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    """Application configuration for organization management."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.organizations"
    label = "organizations"
    verbose_name = "Organizations"
