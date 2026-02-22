"""
JudgeLoom — Core Abstract Models
==================================

Reusable base model classes that enforce consistent patterns across
the entire platform. Every app model should inherit from one of these.

Classes:
    TimestampedModel: Adds created_at / updated_at auto-managed fields.
    SluggedModel: Adds a unique slug with auto-generation support.
    OrderedModel: Adds an integer ``order`` field for manual sorting.
"""

from __future__ import annotations

from django.db import models
from django.utils.text import slugify


class TimestampedModel(models.Model):
    """Abstract base providing auto-managed timestamp fields.

    Fields:
        created_at: Set once on initial save (``auto_now_add``).
        updated_at: Refreshed on every save (``auto_now``).

    All JudgeLoom models should inherit from this to guarantee
    consistent audit-trail columns.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp of record creation.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of last modification.",
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SluggedModel(TimestampedModel):
    """Abstract base adding a unique, URL-safe slug.

    The ``slug`` is auto-generated from ``get_slug_source()`` on first
    save if left blank. Subclasses MUST override ``get_slug_source``.

    Fields:
        slug: Unique, indexed, max 128 characters.
    """

    slug = models.SlugField(
        max_length=128,
        unique=True,
        db_index=True,
        help_text="URL-safe identifier. Auto-generated from the title if blank.",
    )

    class Meta(TimestampedModel.Meta):
        abstract = True

    def get_slug_source(self) -> str:
        """Return the string used to auto-generate the slug.

        Subclasses MUST override this method.

        Returns:
            The human-readable source text (e.g. a title or name).

        Raises:
            NotImplementedError: Always, if not overridden.
        """
        raise NotImplementedError("Subclasses must implement get_slug_source().")

    def save(self, *args: object, **kwargs: object) -> None:
        """Auto-populate slug from ``get_slug_source()`` when blank."""
        if not self.slug:
            base_slug = slugify(self.get_slug_source())[:120]
            slug = base_slug
            counter = 1
            model_class = self.__class__
            while model_class.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class OrderedModel(TimestampedModel):
    """Abstract base adding a manual sort-order field.

    Fields:
        order: Non-negative integer for display ordering.
            Defaults to 0. Lower values sort first.
    """

    order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="Display order. Lower values appear first.",
    )

    class Meta(TimestampedModel.Meta):
        abstract = True
        ordering = ["order", "-created_at"]
