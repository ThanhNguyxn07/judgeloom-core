from __future__ import annotations

from django.db import models

from core.models import TimestampedModel


class Language(TimestampedModel):
    """Programming language metadata available for submissions."""

    key = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=32)
    ace_mode = models.CharField(max_length=64, default="text")
    pygments_name = models.CharField(max_length=64, default="text")
    description = models.CharField(max_length=255, blank=True)
    template = models.TextField(blank=True)
    is_enabled = models.BooleanField(default=True)
    extension = models.CharField(max_length=16)

    class Meta(TimestampedModel.Meta):
        db_table = "judge_language"
        ordering = ["key"]
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        indexes = [
            models.Index(fields=["key"], name="lang_key_idx"),
            models.Index(fields=["is_enabled"], name="lang_enabled_idx"),
            models.Index(fields=["created_at"], name="lang_created_idx"),
        ]

    def __str__(self) -> str:
        """Return language key for admin and logs.

        Returns:
            The unique language key.
        """
        return self.key
