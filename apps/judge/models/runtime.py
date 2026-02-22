from __future__ import annotations

from django.db import models

from core.models import TimestampedModel


class RuntimeVersion(TimestampedModel):
    """Runtime metadata describing language support on each judge."""

    judge = models.ForeignKey("judge.Judge", on_delete=models.CASCADE, related_name="runtime_versions")
    language = models.ForeignKey("judge.Language", on_delete=models.CASCADE, related_name="runtime_versions")
    name = models.CharField(max_length=128)
    version = models.CharField(max_length=64)
    priority = models.IntegerField(default=0)

    class Meta(TimestampedModel.Meta):
        db_table = "judge_runtime_version"
        ordering = ["-priority", "name"]
        verbose_name = "Runtime Version"
        verbose_name_plural = "Runtime Versions"
        unique_together = (("judge", "language"),)
        indexes = [
            models.Index(fields=["judge", "language"], name="rt_judge_lang_idx"),
            models.Index(fields=["priority"], name="rt_priority_idx"),
            models.Index(fields=["created_at"], name="rt_created_idx"),
        ]

    def __str__(self) -> str:
        """Return a concise label for the runtime.

        Returns:
            Runtime and version string.
        """
        return f"{self.name} ({self.version})"
