from __future__ import annotations

from django.db import models


class UserRole(models.TextChoices):
    """Supported user roles in JudgeLoom."""

    PARTICIPANT = "participant", "Participant"
    PROBLEM_SETTER = "problem_setter", "Problem Setter"
    JUDGE = "judge", "Judge"
    ADMIN = "admin", "Admin"


class DisplayTheme(models.TextChoices):
    """UI theme preferences for user profile rendering."""

    SYSTEM = "system", "System"
    LIGHT = "light", "Light"
    DARK = "dark", "Dark"


class LanguageCode(models.TextChoices):
    """Supported profile language preferences."""

    EN = "en", "English"
    VI = "vi", "Vietnamese"


class RatingTier(models.IntegerChoices):
    """Discrete rating tiers used by profile and UI decorations."""

    NEWBIE = 0, "Newbie"
    PUPIL = 1200, "Pupil"
    SPECIALIST = 1400, "Specialist"
    EXPERT = 1600, "Expert"
    CANDIDATE_MASTER = 1900, "Candidate Master"
    MASTER = 2100, "Master"
    GRANDMASTER = 2400, "Grandmaster"
