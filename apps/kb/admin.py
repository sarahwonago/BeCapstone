from django.contrib import admin
from .models import KnowledgeBaseArticle


@admin.register(KnowledgeBaseArticle)
class KnowledgeBaseArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "related_issue", "created_by", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "content", "tags")
