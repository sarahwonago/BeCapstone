from django.db import models
from django.conf import settings
from apps.issues.models import Issue


class KnowledgeBaseArticle(models.Model):
    """Model for knowledge base articles"""

    title = models.CharField(max_length=200)
    content = models.TextField()
    related_issue = models.ForeignKey(
        Issue,
        on_delete=models.SET_NULL,
        related_name="kb_articles",
        null=True,
        blank=True,
    )
    tags = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_kb_articles",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
