from __future__ import annotations

from datetime import datetime

from ninja import Schema


class JudgeOut(Schema):
    """Compact judge representation."""

    name: str
    online: bool
    is_blocked: bool
    status: str
    ping: float | None
    load: float | None


class JudgeDetailOut(JudgeOut):
    """Detailed judge response payload."""

    hostname: str
    description: str
    last_ip: str | None
    start_time: datetime | None
    uptime_seconds: int | None
    languages: list[str]
    problems: list[str]


class LanguageOut(Schema):
    """Language payload used by judge APIs."""

    id: int
    key: str
    name: str
    short_name: str
    ace_mode: str
    pygments_name: str
    description: str
    extension: str
    is_enabled: bool
