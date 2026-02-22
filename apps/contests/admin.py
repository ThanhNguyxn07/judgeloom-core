from __future__ import annotations

from django.contrib import admin

from apps.contests.models import Contest, ContestMoss, ContestParticipation, ContestProblem


class ContestProblemInline(admin.TabularInline):
    """Inline editor for contest problems."""

    model = ContestProblem
    extra = 0


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    """Admin configuration for contests."""

    list_display = (
        "id",
        "key",
        "name",
        "start_time",
        "end_time",
        "visibility",
        "is_rated",
        "format_name",
        "is_visible",
    )
    list_filter = ("visibility", "is_rated", "format_name", "is_visible")
    search_fields = ("key", "name", "slug")
    filter_horizontal = (
        "organizers",
        "curators",
        "testers",
        "organizations",
        "rate_exclude",
        "banned_users",
    )
    inlines = (ContestProblemInline,)


@admin.register(ContestProblem)
class ContestProblemAdmin(admin.ModelAdmin):
    """Admin configuration for contest problem mapping."""

    list_display = ("id", "contest", "label", "problem", "order", "points", "partial_score")
    list_filter = ("partial_score",)
    search_fields = ("contest__key", "label", "problem__title")


@admin.register(ContestParticipation)
class ContestParticipationAdmin(admin.ModelAdmin):
    """Admin configuration for contest participations."""

    list_display = (
        "id",
        "contest",
        "user",
        "status",
        "score",
        "cumulative_time",
        "is_disqualified",
    )
    list_filter = ("status", "is_disqualified")
    search_fields = ("contest__key", "user__username")


@admin.register(ContestMoss)
class ContestMossAdmin(admin.ModelAdmin):
    """Admin configuration for contest MOSS runs."""

    list_display = ("id", "contest", "problem", "language", "status", "created_at")
    list_filter = ("status", "language")
    search_fields = ("contest__key", "problem__title")
