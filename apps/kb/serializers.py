from rest_framework import serializers
from .models import KnowledgeBaseArticle
from apps.issues.serializers import IssueListSerializer
from apps.users.serializers import UserBriefSerializer


class KnowledgeBaseArticleSerializer(serializers.ModelSerializer):
    """Serializer for knowledge base articles"""

    created_by_details = UserBriefSerializer(source="created_by", read_only=True)
    related_issue_details = IssueListSerializer(source="related_issue", read_only=True)
    tags_list = serializers.SerializerMethodField()

    class Meta:
        model = KnowledgeBaseArticle
        fields = [
            "id",
            "title",
            "content",
            "related_issue",
            "related_issue_details",
            "tags",
            "tags_list",
            "created_by",
            "created_by_details",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "created_by_details",
            "related_issue_details",
        ]

    def get_tags_list(self, obj):
        """Convert comma-separated tags to a list"""
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(",") if tag.strip()]
        return []

    def create(self, validated_data):
        """Set the created_by field to the current user"""
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
