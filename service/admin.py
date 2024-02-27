from django.contrib import admin

from service import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "phone"]
    search_fields = ["first_name", "last_name", "phone"]


@admin.register(models.Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name"]
    search_fields = ["first_name", "last_name"]


@admin.register(models.Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ["id", "body", "status", "client", "processed_by"]
    search_fields = ["body"]
    list_filter = ["status"]
    list_select_related = ["client", "processed_by"]
    raw_id_fields = ["client", "processed_by"]
    autocomplete_fields = ["client", "processed_by"]
    actions = ["mark_as_completed", "mark_as_rejected"]

    def mark_as_completed(self, request, queryset):
        queryset.update(status=models.RequestStatus.Completed)

    def mark_as_rejected(self, request, queryset):
        queryset.update(status=models.RequestStatus.Rejected)

    mark_as_completed.short_description = "Mark selected requests as completed"
    mark_as_rejected.short_description = "Mark selected requests as rejected"
