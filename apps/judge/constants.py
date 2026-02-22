from __future__ import annotations

from django.db import models


class JudgeStatus(models.TextChoices):
    """Judge availability states."""

    AVAILABLE = "AV", "Available (AV)"
    BUSY = "BU", "Busy (BU)"
    OFFLINE = "OF", "Offline (OF)"
    DISABLED = "DI", "Disabled (DI)"
