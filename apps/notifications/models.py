from django.db import models
from django.conf import settings


class Notification(models.Model):
    """Model for user notifications"""

    # Notification types
    ISSUE_CREATED = "issue_created"
    ISSUE_ASSIGNED = "issue_assigned"
    ISSUE_UPDATED = "issue_updated"
    ISSUE_RESOLVED = "issue_resolved"
    COMMENT_ADDED = "comment_added"
    FEEDBACK_ADDED = "feedback_added"

    NOTIFICATION_TYPES = (
        (ISSUE_CREATED, "Issue Created"),
        (ISSUE_ASSIGNED, "Issue Assigned"),
        (ISSUE_UPDATED, "Issue Updated"),
        (ISSUE_RESOLVED, "Issue Resolved"),
        (COMMENT_ADDED, "Comment Added"),
        (FEEDBACK_ADDED, "Feedback Added"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    issue = models.ForeignKey(
        "issues.Issue",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    message = models.CharField(max_length=255)
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES, default=ISSUE_UPDATED
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}..."
