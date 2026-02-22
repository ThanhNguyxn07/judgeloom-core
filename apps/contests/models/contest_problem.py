from __future__ import annotations

from django.db import models

from core.models import TimestampedModel


class ContestProblem(TimestampedModel):
    """Mapping between a contest and a problem with display/scoring metadata."""

    contest = models.ForeignKey("contests.Contest", on_delete=models.CASCADE, related_name="contest_problems")
    problem = models.ForeignKey("problems.Problem", on_delete=models.CASCADE, related_name="problem_contests")
    order = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=10)
    points = models.FloatField(default=0.0)
    partial_score = models.BooleanField(default=False)
    output_prefix_override = models.IntegerField(null=True, blank=True)
    max_submissions = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "contests_contest_problem"
        verbose_name = "Contest Problem"
        verbose_name_plural = "Contest Problems"
        ordering = ["order"]
        unique_together = (("contest", "problem"), ("contest", "label"))
        indexes = [
            models.Index(fields=["contest", "order"], name="contest_problem_order_idx"),
            models.Index(fields=["contest", "label"], name="contest_problem_label_idx"),
        ]

    def __str__(self) -> str:
        """Return concise contest problem label."""

        return f"{self.contest.key}:{self.label}"
