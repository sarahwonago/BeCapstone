from rest_framework import serializers
from django.contrib.auth import get_user_model
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
from drf_spectacular.utils import extend_schema_field

User = get_user_model()


class UserBriefSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for User model to use in nested representations.
    """

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "role", "cohort"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    """

    class Meta:
        model = Course
        fields = ["id", "name", "duration_in_weeks", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for Project model.
    """

    course_name = serializers.CharField(source="course.name", read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "course",
            "course_name",
            "week_number",
            "total_tasks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "course_name"]


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    """

    project_name = serializers.CharField(source="project.name", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "project_name",
            "task_number",
            "title",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "project_name"]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    """

    user_details = UserBriefSerializer(source="user", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "issue",
            "user",
            "user_details",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "user_details"]

    def create(self, validated_data):
        # Set the user to the current user
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class AttachmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Attachment model.
    """

    file_url = serializers.SerializerMethodField()
    uploaded_by_username = serializers.CharField(
        source="uploaded_by.username", read_only=True
    )
    file_size_display = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            "id",
            "issue",
            "file",
            "file_url",
            "file_name",
            "content_type",
            "file_size",
            "file_size_display",
            "uploaded_by",
            "uploaded_by_username",
            "uploaded_at",
        ]
        read_only_fields = [
            "uploaded_at",
            "uploaded_by_username",
            "file_name",
            "file_url",
            "content_type",
            "file_size",
            "file_size_display",
        ]
        extra_kwargs = {
            "file": {"write_only": True}  # Hide actual file path in response
        }

    def get_file_url(self, obj):
        """Return the URL to download the file"""
        if obj.file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None

    def get_file_size_display(self, obj):
        """Return human-readable file size"""
        size_bytes = obj.file_size

        # Handle edge cases
        if size_bytes < 0:
            return "0 bytes"

        # Define size units
        units = ["bytes", "KB", "MB", "GB", "TB"]
        size = float(size_bytes)
        unit_index = 0

        # Find the appropriate unit
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        # Format with 2 decimal places if not bytes
        if unit_index == 0:
            return f"{int(size)} {units[unit_index]}"
        else:
            return f"{size:.2f} {units[unit_index]}"

    def validate_file(self, file):
        """Validate the uploaded file"""
        from .utils import validate_file_size, validate_file_type

        # Validate file size
        validate_file_size(file)

        # Validate file type
        validate_file_type(file)

        return file

    def create(self, validated_data):
        # Set the uploaded_by to the current user
        validated_data["uploaded_by"] = self.context["request"].user
        return super().create(validated_data)


class IssueFeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for IssueFeedback model.
    """

    class Meta:
        model = IssueFeedback
        fields = ["id", "issue", "rating", "comment", "created_at"]
        read_only_fields = ["created_at"]


class IssueHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for IssueHistory model.
    """

    performed_by_details = UserBriefSerializer(source="performed_by", read_only=True)

    class Meta:
        model = IssueHistory
        fields = [
            "id",
            "issue",
            "action",
            "performed_by",
            "performed_by_details",
            "timestamp",
        ]
        read_only_fields = ["timestamp", "performed_by_details"]


class IssueTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for IssueTemplate model.
    """

    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    category_display = serializers.CharField(
        source="get_category_display", read_only=True
    )

    class Meta:
        model = IssueTemplate
        fields = [
            "id",
            "title",
            "description_template",
            "category",
            "category_display",
            "created_by",
            "created_by_username",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "created_by_username",
            "category_display",
        ]

    def create(self, validated_data):
        # Set the created_by to the current user
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class IssueListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing Issues.
    """

    reported_by_details = UserBriefSerializer(source="reported_by", read_only=True)
    assigned_to_details = UserBriefSerializer(source="assigned_to", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    task_title = serializers.CharField(source="task.title", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    category_display = serializers.CharField(
        source="get_category_display", read_only=True
    )
    urgency_display = serializers.CharField(
        source="get_urgency_display", read_only=True
    )
    comments_count = serializers.SerializerMethodField()
    attachments_count = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "status",
            "status_display",
            "category",
            "category_display",
            "urgency",
            "urgency_display",
            "reported_by",
            "reported_by_details",
            "assigned_to",
            "assigned_to_details",
            "course",
            "course_name",
            "project",
            "project_name",
            "task",
            "task_title",
            "cohort",
            "week_number",
            "created_at",
            "updated_at",
            "first_response_at",
            "resolved_at",
            "comments_count",
            "attachments_count",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "reported_by_details",
            "assigned_to_details",
            "course_name",
            "project_name",
            "task_title",
            "status_display",
            "category_display",
            "urgency_display",
            "first_response_at",
            "resolved_at",
            "comments_count",
            "attachments_count",
        ]

    @extend_schema_field(serializers.IntegerField())
    def get_comments_count(self, obj):
        return obj.comments.count()

    @extend_schema_field(serializers.IntegerField())
    def get_attachments_count(self, obj):
        return obj.attachments.count()


class IssueDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Issue model with nested relationships.
    """

    reported_by_details = UserBriefSerializer(source="reported_by", read_only=True)
    assigned_to_details = UserBriefSerializer(source="assigned_to", read_only=True)
    course_details = CourseSerializer(source="course", read_only=True)
    project_details = ProjectSerializer(source="project", read_only=True)
    task_details = TaskSerializer(source="task", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    history = IssueHistorySerializer(many=True, read_only=True)
    feedback = IssueFeedbackSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    category_display = serializers.CharField(
        source="get_category_display", read_only=True
    )
    urgency_display = serializers.CharField(
        source="get_urgency_display", read_only=True
    )

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "status",
            "status_display",
            "category",
            "category_display",
            "urgency",
            "urgency_display",
            "reported_by",
            "reported_by_details",
            "assigned_to",
            "assigned_to_details",
            "course",
            "course_details",
            "project",
            "project_details",
            "task",
            "task_details",
            "cohort",
            "week_number",
            "created_at",
            "updated_at",
            "first_response_at",
            "resolved_at",
            "comments",
            "attachments",
            "history",
            "feedback",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "reported_by_details",
            "assigned_to_details",
            "course_details",
            "project_details",
            "task_details",
            "status_display",
            "category_display",
            "urgency_display",
            "first_response_at",
            "resolved_at",
            "comments",
            "attachments",
            "history",
            "feedback",
        ]


class IssueCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Issues.
    """

    class Meta:
        model = Issue
        fields = [
            "title",
            "description",
            "category",
            "urgency",
            "course",
            "project",
            "task",
            "cohort",
            "week_number",
        ]

    def create(self, validated_data):
        # Set the reported_by to the current user
        validated_data["reported_by"] = self.context["request"].user
        # Status is automatically set to OPEN by the model default
        return super().create(validated_data)


class IssueUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Issues.
    """

    class Meta:
        model = Issue
        fields = ["status", "assigned_to"]

    def update(self, instance, validated_data):
        # Track status changes
        if "status" in validated_data and validated_data["status"] != instance.status:
            # If changing to IN_PROGRESS and first_response_at is not set
            if (
                validated_data["status"] == Issue.IN_PROGRESS
                and not instance.first_response_at
            ):
                from django.utils import timezone

                validated_data["first_response_at"] = timezone.now()

            # If changing to RESOLVED
            if validated_data["status"] == Issue.RESOLVED:
                from django.utils import timezone

                validated_data["resolved_at"] = timezone.now()

            # Create history entry for status change
            user = self.context["request"].user
            IssueHistory.objects.create(
                issue=instance,
                action=f"Changed status from '{instance.get_status_display()}' to '{dict(Issue.STATUS_CHOICES).get(validated_data['status'])}'",
                performed_by=user,
            )

        # Track assignment changes
        if (
            "assigned_to" in validated_data
            and validated_data["assigned_to"] != instance.assigned_to
        ):
            user = self.context["request"].user
            new_assignee = validated_data["assigned_to"]
            IssueHistory.objects.create(
                issue=instance,
                action=f"Assigned issue to {new_assignee.username if new_assignee else 'no one'}",
                performed_by=user,
            )

        return super().update(instance, validated_data)
