from __future__ import annotations

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Application configuration for account and authentication features."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    label = "accounts"
    verbose_name = "Accounts"
