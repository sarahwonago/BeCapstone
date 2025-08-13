from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "issue", "type", "is_read", "created_at")
    list_filter = ("is_read", "type", "created_at")
    search_fields = ("message",)
