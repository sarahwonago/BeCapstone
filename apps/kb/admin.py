from django.contrib import admin
from .models import KnowledgeBaseArticle


@admin.register(KnowledgeBaseArticle)
class KnowledgeBaseArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "related_issue", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title", "content", "tags")
    raw_id_fields = ("related_issue", "created_by")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "content", "tags")}),
        ("Related Data", {"fields": ("related_issue", "created_by")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
