from __future__ import annotations

from django.db import models

from core.models import TimestampedModel


class SubmissionSource(TimestampedModel):
    """Stores the original source code for a submission."""

    submission = models.OneToOneField(
        "submissions.Submission",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="source",
    )
    source_code = models.TextField()

    class Meta(TimestampedModel.Meta):
        db_table = "submissions_source"
        ordering = ["-created_at"]
        verbose_name = "Submission Source"
        verbose_name_plural = "Submission Sources"
        indexes = [models.Index(fields=["created_at"], name="subsrc_created_idx")]

    def __str__(self) -> str:
        """Return a concise identifier for admin and logs.

        Returns:
            A string representation containing the submission id.
        """
        return f"SubmissionSource(submission_id={self.submission_id})"
