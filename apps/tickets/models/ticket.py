from __future__ import annotations

from django.db import models

from apps.tickets.constants import TicketPriority, TicketStatus
from core.models import TimestampedModel


class Ticket(TimestampedModel):
    """User-submitted support ticket."""

    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    assignees = models.ManyToManyField(
        "accounts.User",
        related_name="assigned_tickets",
        blank=True,
    )
    linked_problem = models.ForeignKey(
        "problems.Problem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )
    linked_contest = models.ForeignKey(
        "contests.Contest",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )
    body = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN,
    )
    priority = models.CharField(
        max_length=16,
        choices=TicketPriority.choices,
        default=TicketPriority.MEDIUM,
    )
    is_public = models.BooleanField(default=True)

    @property
    def is_open(self) -> bool:
        """Return True when ticket is in an active open state."""

        return self.status in {TicketStatus.OPEN, TicketStatus.IN_PROGRESS}

    @property
    def is_resolved(self) -> bool:
        """Return True when ticket is in a terminal resolved state."""

        return self.status in {TicketStatus.RESOLVED, TicketStatus.CLOSED}

    def __str__(self) -> str:
        """Return human-readable ticket label."""

        return f"Ticket #{self.pk}: {self.title}"

    class Meta:
        db_table = "tickets_ticket"
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status"], name="tickets_status_idx"),
            models.Index(fields=["priority"], name="tickets_priority_idx"),
            models.Index(fields=["author"], name="tickets_author_idx"),
        ]
