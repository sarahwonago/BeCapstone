from django.contrib import admin
from .models import (
    Course,
    Project,
    Task,
    Issue,
    Comment,
    IssueFeedback,
    IssueHistory,
    Attachment,
    IssueTemplate,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_in_weeks", "created_at")
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "week_number", "total_tasks")
    list_filter = ("course", "week_number")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "task_number")
    list_filter = ("project",)
    search_fields = ("title",)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "category",
        "urgency",
        "reported_by",
        "assigned_to",
        "created_at",
    )
    list_filter = ("status", "category", "urgency", "cohort")
    search_fields = ("title", "description")
    date_hierarchy = "created_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("issue", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content",)


@admin.register(IssueFeedback)
class IssueFeedbackAdmin(admin.ModelAdmin):
    list_display = ("issue", "rating", "created_at")
    list_filter = ("rating",)


@admin.register(IssueHistory)
class IssueHistoryAdmin(admin.ModelAdmin):
    list_display = ("issue", "action", "performed_by", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("action",)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("issue", "file_name", "uploaded_by", "uploaded_at")
    list_filter = ("uploaded_at",)
    search_fields = ("file_name",)


@admin.register(IssueTemplate)
class IssueTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_by", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description_template")
