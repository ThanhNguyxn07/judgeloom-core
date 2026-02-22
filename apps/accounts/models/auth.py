from __future__ import annotations

from django.db import models

from core.models import TimestampedModel


class WebAuthnCredential(TimestampedModel):
    """Registered passkey credential linked to a user account."""

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="webauthn_credentials",
    )
    credential_id = models.BinaryField(unique=True)
    public_key = models.BinaryField()
    sign_count = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=128)

    class Meta(TimestampedModel.Meta):
        """Model metadata and credential lookup indexes."""

        db_table = "accounts_webauthn_credential"
        ordering = ["-created_at"]
        verbose_name = "WebAuthn Credential"
        verbose_name_plural = "WebAuthn Credentials"
        indexes = [
            models.Index(fields=["user"], name="accounts_webauthn_user_idx"),
            models.Index(fields=["created_at"], name="accounts_webauthn_created_idx"),
        ]

    def __str__(self) -> str:
        """Return concise admin display string."""

        return f"{self.user.username}:{self.name}"
