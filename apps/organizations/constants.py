from __future__ import annotations

from django.db import models


class OrganizationRequestStatus(models.TextChoices):
    """Review state for organization membership requests."""

    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
