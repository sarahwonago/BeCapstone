from rest_framework import serializers
from .models import Notification
from apps.issues.serializers import IssueListSerializer
from apps.users.serializers import UserBriefSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""

    issue_details = serializers.SerializerMethodField(read_only=True)
    notification_type_display = serializers.CharField(
        source="get_notification_type_display", read_only=True
    )
    time_since = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "issue",
            "issue_details",
            "message",
            "notification_type",
            "notification_type_display",
            "is_read",
            "created_at",
            "time_since",
        ]
        read_only_fields = [
            "user",
            "issue",
            "message",
            "notification_type",
            "created_at",
            "issue_details",
            "notification_type_display",
            "time_since",
        ]

    def get_issue_details(self, obj):
        """Return minimal issue details if issue exists"""
        if obj.issue:
            return {
                "id": obj.issue.id,
                "title": obj.issue.title,
                "status": obj.issue.status,
                "status_display": obj.issue.get_status_display(),
            }
        return None

    def get_time_since(self, obj):
        """Return human-readable time since notification creation"""
        from django.utils import timezone
        from django.utils.timesince import timesince

        return timesince(obj.created_at, timezone.now())
