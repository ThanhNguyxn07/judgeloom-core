from __future__ import annotations

from django.db import models


class ContestVisibility(models.TextChoices):
    """Visibility levels for contests."""

    PRIVATE = "private", "Private"
    ORGANIZATION = "organization", "Organization"
    PUBLIC = "public", "Public"


class ParticipationStatus(models.TextChoices):
    """Participation mode/status for a contestant."""

    LIVE = "live", "Live"
    SPECTATING = "spectating", "Spectating"
    VIRTUAL = "virtual", "Virtual"


class ContestFormat(models.TextChoices):
    """Supported contest scoring formats."""

    DEFAULT = "default", "Default"
    ICPC = "icpc", "ICPC"
    IOI = "ioi", "IOI"
    ATCODER = "atcoder", "AtCoder"
    ECOO = "ecoo", "ECOO"
