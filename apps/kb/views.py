from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)

from .models import KnowledgeBaseArticle
from .serializers import KnowledgeBaseArticleSerializer
from apps.users.permissions import IsMentorOrAdmin, IsOwnerOrMentorOrAdmin


@extend_schema_view(
    list=extend_schema(
        summary="List knowledge base articles",
        description="List all knowledge base articles with optional filtering.",
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search articles by title or content",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="tags",
                description="Filter articles by tag",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="related_issue",
                description="Filter articles by related issue ID",
                required=False,
                type=int,
            ),
        ],
        responses={
            200: KnowledgeBaseArticleSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    ),
    create=extend_schema(
        summary="Create knowledge base article",
        description="Create a new knowledge base article. Only accessible to mentors and admins.",
        responses={
            201: KnowledgeBaseArticleSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve knowledge base article",
        description="Retrieve a specific knowledge base article.",
        responses={
            200: KnowledgeBaseArticleSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            404: OpenApiResponse(description="Article not found."),
        },
    ),
    update=extend_schema(
        summary="Update knowledge base article",
        description="Update a knowledge base article. Only accessible to the creator, mentors, and admins.",
        responses={
            200: KnowledgeBaseArticleSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to update this article."
            ),
            404: OpenApiResponse(description="Article not found."),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update knowledge base article",
        description="Partially update a knowledge base article. Only accessible to the creator, mentors, and admins.",
        responses={
            200: KnowledgeBaseArticleSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to update this article."
            ),
            404: OpenApiResponse(description="Article not found."),
        },
    ),
    destroy=extend_schema(
        summary="Delete knowledge base article",
        description="Delete a knowledge base article. Only accessible to the creator, mentors, and admins.",
        responses={
            204: OpenApiResponse(description="Article deleted successfully."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to delete this article."
            ),
            404: OpenApiResponse(description="Article not found."),
        },
    ),
)
class KnowledgeBaseArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing knowledge base articles.
    """

    queryset = KnowledgeBaseArticle.objects.all()
    serializer_class = KnowledgeBaseArticleSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["related_issue"]
    search_fields = ["title", "content", "tags"]
    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsMentorOrAdmin()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsOwnerOrMentorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by tags if provided
        tags = self.request.query_params.get("tags")
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
            # Construct a query to find articles containing any of the specified tags
            from django.db.models import Q

            tag_query = Q()
            for tag in tag_list:
                tag_query |= Q(tags__icontains=tag)
            queryset = queryset.filter(tag_query)

        return queryset
