from django.db import models
from django.conf import settings
from apps.issues.models import Issue


class Notification(models.Model):
    """Model for user notifications"""

    # Notification types
    ISSUE_CREATED = "issue_created"
    ISSUE_ASSIGNED = "issue_assigned"
    COMMENT_ADDED = "comment_added"
    STATUS_CHANGED = "status_changed"
    ISSUE_RESOLVED = "issue_resolved"

    TYPE_CHOICES = [
        (ISSUE_CREATED, "Issue Created"),
        (ISSUE_ASSIGNED, "Issue Assigned"),
        (COMMENT_ADDED, "Comment Added"),
        (STATUS_CHANGED, "Status Changed"),
        (ISSUE_RESOLVED, "Issue Resolved"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

    class Meta:
        ordering = ["-created_at"]
