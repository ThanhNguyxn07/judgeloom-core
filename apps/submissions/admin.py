from __future__ import annotations

from django.contrib import admin

from apps.submissions.models import Submission, SubmissionSource, SubmissionTestCase


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """Admin configuration for submission records."""

    list_display = (
        "id",
        "user",
        "problem",
        "language",
        "status",
        "result",
        "points",
        "created_at",
    )
    list_filter = ("status", "result", "language", "created_at")
    search_fields = ("id", "user__username", "problem__code")
    autocomplete_fields = ("user", "problem", "language", "contest_participation", "judged_on")
    readonly_fields = ("created_at", "updated_at", "judged_at")


@admin.register(SubmissionSource)
class SubmissionSourceAdmin(admin.ModelAdmin):
    """Admin configuration for submission source code."""

    list_display = ("submission", "created_at", "updated_at")
    search_fields = ("submission__id",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(SubmissionTestCase)
class SubmissionTestCaseAdmin(admin.ModelAdmin):
    """Admin configuration for test-case level results."""

    list_display = (
        "submission",
        "case_number",
        "status",
        "time_used",
        "memory_used",
        "points",
    )
    list_filter = ("status", "created_at")
    search_fields = ("submission__id",)
    autocomplete_fields = ("submission",)
    readonly_fields = ("created_at", "updated_at")
