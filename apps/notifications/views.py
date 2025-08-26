from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)

from .models import Notification
from .serializers import NotificationSerializer
from apps.users.permissions import IsOwnerOrAdmin


@extend_schema_view(
    list=extend_schema(
        summary="List notifications",
        description="List notifications for the current user.",
        responses={
            200: NotificationSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve notification",
        description="Retrieve a specific notification.",
        responses={
            200: NotificationSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to access this notification."
            ),
            404: OpenApiResponse(description="Notification not found."),
        },
    ),
)
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing notifications.
    """

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["is_read", "notification_type"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Return notifications for the current user only"""
        return Notification.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Mark notification as read",
        description="Mark a specific notification as read.",
        responses={
            200: NotificationSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to update this notification."
            ),
            404: OpenApiResponse(description="Notification not found."),
        },
    )
    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        """Mark a notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

    @extend_schema(
        summary="Mark all notifications as read",
        description="Mark all notifications for the current user as read.",
        responses={
            200: OpenApiResponse(description="All notifications marked as read."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    )
    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().update(is_read=True)
        return Response({"detail": "All notifications marked as read."})

    @extend_schema(
        summary="Unread count",
        description="Get the count of unread notifications for the current user.",
        responses={
            200: OpenApiResponse(description="Count of unread notifications."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    )
    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({"unread_count": count})
