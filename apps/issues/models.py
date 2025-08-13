from django.db import models
from django.conf import settings


class Course(models.Model):
    """Model for courses in the curriculum"""

    name = models.CharField(max_length=100)
    duration_in_weeks = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Project(models.Model):
    """Model for projects within courses"""

    name = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="projects"
    )
    week_number = models.PositiveIntegerField()
    total_tasks = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Week {self.week_number}"

    class Meta:
        ordering = ["course", "week_number"]
        unique_together = ["course", "name", "week_number"]


class Task(models.Model):
    """Model for individual tasks within projects"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    task_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name} - Task {self.task_number}: {self.title}"

    class Meta:
        ordering = ["project", "task_number"]
        unique_together = ["project", "task_number"]


class Issue(models.Model):
    """Model for curriculum issues reported by students"""

    # Status choices
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"

    STATUS_CHOICES = [
        (OPEN, "Open"),
        (IN_PROGRESS, "In Progress"),
        (RESOLVED, "Resolved"),
    ]

    # Category choices
    CHECKER_ERROR = "checker_error"
    UNCLEAR_INSTRUCTIONS = "unclear_instructions"
    TYPO = "typo"
    TECHNICAL_ERROR = "technical_error"
    OTHER = "other"

    CATEGORY_CHOICES = [
        (CHECKER_ERROR, "Checker Error"),
        (UNCLEAR_INSTRUCTIONS, "Unclear Instructions"),
        (TYPO, "Typo"),
        (TECHNICAL_ERROR, "Technical Error"),
        (OTHER, "Other"),
    ]

    # Urgency choices
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    URGENCY_CHOICES = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    ]

    # Core fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default=MEDIUM)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=OPEN)

    # Relationships
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reported_issues",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_issues",
        null=True,
        blank=True,
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="issues")
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues"
    )
    task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, related_name="issues", null=True, blank=True
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_response_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    # Additional metadata
    cohort = models.CharField(max_length=50)
    week_number = models.PositiveIntegerField()

    def __str__(self):
        return f"Issue #{self.id}: {self.title} ({self.status})"

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["category"]),
            models.Index(fields=["cohort"]),
            models.Index(fields=["created_at"]),
        ]


class Comment(models.Model):
    """Model for comments on issues"""

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on Issue #{self.issue.id}"

    class Meta:
        ordering = ["created_at"]


class IssueFeedback(models.Model):
    """Model for feedback on resolved issues"""

    issue = models.OneToOneField(
        Issue, on_delete=models.CASCADE, related_name="feedback"
    )
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],  # 1-5 rating
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Issue #{self.issue.id}: {self.rating}/5"


class IssueHistory(models.Model):
    """Model for tracking issue history and actions"""

    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="history")
    action = models.CharField(max_length=255)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="issue_actions",
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue #{self.issue.id}: {self.action} by {self.performed_by.username}"

    class Meta:
        ordering = ["-timestamp"]
        verbose_name_plural = "Issue histories"


def issue_attachment_path(instance, filename):
    """Define upload path for issue attachments"""
    return f"attachments/issues/{instance.issue.id}/{filename}"


class Attachment(models.Model):
    """Model for file attachments on issues"""

    issue = models.ForeignKey(
        Issue, on_delete=models.CASCADE, related_name="attachments"
    )
    file = models.FileField(upload_to=issue_attachment_path)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_attachments",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Attachment for Issue #{self.issue.id}: {self.file_name}"

    def save(self, *args, **kwargs):
        if not self.file_name and self.file:
            self.file_name = self.file.name
        super().save(*args, **kwargs)


class IssueTemplate(models.Model):
    """Model for issue templates"""

    title = models.CharField(max_length=200)
    description_template = models.TextField()
    category = models.CharField(
        max_length=50,
        choices=Issue.CATEGORY_CHOICES,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_templates",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Template: {self.title} ({self.category})"
