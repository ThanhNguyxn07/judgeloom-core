from __future__ import annotations

from ninja import Schema
from pydantic import EmailStr, Field


class UserRegisterIn(Schema):
    """Payload used to register a new account."""

    username: str = Field(min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLoginIn(Schema):
    """Credentials for user login."""

    username_or_email: str = Field(min_length=1, max_length=254)
    password: str = Field(min_length=1, max_length=128)


class TokenOut(Schema):
    """JWT authentication response."""

    access_token: str
    token_type: str = "Bearer"


class UserProfileOut(Schema):
    """Detailed user profile for authenticated endpoints."""

    username: str
    email: str
    display_name: str
    timezone: str
    language: str
    theme: str
    display_rank: str
    about: str
    rating: int
    max_rating: int
    points: float
    performance_points: float
    problem_count: int
    is_totp_enabled: bool
    mfa_enabled: bool
    css_class: str
    is_banned: bool


class UserUpdateIn(Schema):
    """Partial profile update payload."""

    timezone: str | None = None
    language: str | None = None
    theme: str | None = None
    display_rank: str | None = None
    about: str | None = None
    notes: str | None = None


class UserStatsOut(Schema):
    """Aggregated user statistic payload."""

    submission_count: int
    solved_problem_count: int
    rating: int
    max_rating: int
    points: float
    performance_points: float
    problem_count: int
    contributions: float


class UserPublicOut(Schema):
    """Publicly visible user profile payload."""

    username: str
    display_name: str
    rating: int
    max_rating: int
    points: float
    problem_count: int
    css_class: str
