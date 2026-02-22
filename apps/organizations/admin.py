from __future__ import annotations

from django.contrib import admin

from apps.organizations.models import Organization, OrganizationRequest


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin configuration for organizations."""

    list_display = ("name", "slug", "is_open", "creation_date")
    list_filter = ("is_open",)
    search_fields = ("name", "slug", "short_name")
    filter_horizontal = ("admins",)
    readonly_fields = ("creation_date", "created_at", "updated_at")


@admin.register(OrganizationRequest)
class OrganizationRequestAdmin(admin.ModelAdmin):
    """Admin configuration for organization membership requests."""

    list_display = ("organization", "user", "status", "created_at", "reviewed_by")
    list_filter = ("status", "created_at")
    search_fields = ("organization__name", "user__username")
    readonly_fields = ("created_at", "updated_at", "reviewed_at")
