from __future__ import annotations

from django.contrib import admin

from apps.ratings.models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Admin configuration for contest ratings."""

    list_display = (
        "id",
        "contest",
        "user",
        "rank",
        "rating_before",
        "rating_after",
        "performance",
        "created_at",
    )
    list_filter = ("contest",)
    search_fields = ("contest__key", "user__username")
