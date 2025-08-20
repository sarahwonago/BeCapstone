from rest_framework import viewsets, permissions, status, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework.parsers import MultiPartParser, FormParser

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
from .serializers import (
    CourseSerializer,
    ProjectSerializer,
    TaskSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    IssueCreateSerializer,
    IssueUpdateSerializer,
    CommentSerializer,
    IssueFeedbackSerializer,
    AttachmentSerializer,
    IssueTemplateSerializer,
)
from apps.users.permissions import (
    IsAdmin,
    IsMentor,
    IsStudent,
    IsMentorOrAdmin,
    IsOwnerOrMentorOrAdmin,
)

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        summary="List all courses",
        description="List all courses in the curriculum.",
        responses={
            200: CourseSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve a course",
        description="Retrieve details of a specific course.",
        responses={
            200: CourseSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            404: OpenApiResponse(description="Course not found."),
        },
    ),
    create=extend_schema(
        summary="Create a course",
        description="Create a new course. Only accessible to admins.",
        responses={
            201: CourseSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
        },
    ),
    update=extend_schema(
        summary="Update a course",
        description="Update a course. Only accessible to admins.",
        responses={
            200: CourseSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="Course not found."),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update a course",
        description="Partially update a course. Only accessible to admins.",
        responses={
            200: CourseSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="Course not found."),
        },
    ),
    destroy=extend_schema(
        summary="Delete a course",
        description="Delete a course. Only accessible to admins.",
        responses={
            204: OpenApiResponse(description="Course deleted successfully."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="Course not found."),
        },
    ),
)
class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing courses.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "duration_in_weeks", "created_at"]
    ordering = ["name"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]


@extend_schema_view(
    list=extend_schema(
        summary="List all projects",
        description="List all projects in the curriculum.",
        parameters=[
            OpenApiParameter(
                name="course",
                description="Filter projects by course ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="week_number",
                description="Filter projects by week number",
                required=False,
                type=int,
            ),
        ],
        responses={
            200: ProjectSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve a project",
        description="Retrieve details of a specific project.",
        responses={
            200: ProjectSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            404: OpenApiResponse(description="Project not found."),
        },
    ),
    create=extend_schema(
        summary="Create a project",
        description="Create a new project. Only accessible to admins.",
        responses={
            201: ProjectSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
        },
    ),
    update=extend_schema(
        summary="Update a project",
        description="Update a project. Only accessible to admins.",
        responses={
            200: ProjectSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="Project not found."),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update a project",
        description="Partially update a project. Only accessible to admins.",
        responses={
            200: ProjectSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="Project not found."),
        },
    ),
    destroy=extend_schema(
        summary="Delete a project",
        description="Delete a project. Only accessible to admins.",
        responses={
            204: OpenApiResponse(description="Project deleted successfully."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="Project not found."),
        },
    ),
)
class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing projects.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["course", "week_number"]
    search_fields = ["name"]
    ordering_fields = ["name", "course", "week_number", "created_at"]
    ordering = ["course", "week_number"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]


@extend_schema_view(
    list=extend_schema(
        summary="List all tasks",
        description="List all tasks in the curriculum.",
        parameters=[
            OpenApiParameter(
                name="project",
                description="Filter tasks by project ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="task_number",
                description="Filter tasks by task number",
                required=False,
                type=int,
            ),
        ],
        responses={
            200: TaskSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve a task",
        description="Retrieve details of a specific task.",
        responses={
            200: TaskSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            404: OpenApiResponse(description="Task not found."),
        },
    ),
    create=extend_schema(
        summary="Create a task",
        description="Create a new task. Only accessible to admins.",
        responses={
            201: TaskSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
        },
    ),
    update=extend_schema(
        summary="Update a task",
        description="Update a task. Only accessible to admins.",
        responses={
            200: TaskSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="Task not found."),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update a task",
        description="Partially update a task. Only accessible to admins.",
        responses={
            200: TaskSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="Task not found."),
        },
    ),
    destroy=extend_schema(
        summary="Delete a task",
        description="Delete a task. Only accessible to admins.",
        responses={
            204: OpenApiResponse(description="Task deleted successfully."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="Task not found."),
        },
    ),
)
class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["project", "task_number"]
    search_fields = ["title"]
    ordering_fields = ["project", "task_number", "created_at"]
    ordering = ["project", "task_number"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]


@extend_schema_view(
    list=extend_schema(
        summary="List issues",
        description="List issues. Students can only see their own issues, mentors can see issues for their cohort, admins can see all issues.",
        parameters=[
            OpenApiParameter(
                name="status",
                description="Filter issues by status",
                required=False,
                type=str,
                enum=["open", "in_progress", "resolved"],
            ),
            OpenApiParameter(
                name="category",
                description="Filter issues by category",
                required=False,
                type=str,
                enum=[
                    "checker_error",
                    "unclear_instructions",
                    "typo",
                    "technical_error",
                    "other",
                ],
            ),
            OpenApiParameter(
                name="urgency",
                description="Filter issues by urgency",
                required=False,
                type=str,
                enum=["low", "medium", "high"],
            ),
            OpenApiParameter(
                name="course",
                description="Filter issues by course ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="project",
                description="Filter issues by project ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="task",
                description="Filter issues by task ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="cohort",
                description="Filter issues by cohort",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="week_number",
                description="Filter issues by week number",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="reported_by",
                description="Filter issues by reporter user ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="assigned_to",
                description="Filter issues by assignee user ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="search",
                description="Search issues by title or description",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="ordering",
                description="Order issues by field (prefix with '-' for descending order)",
                required=False,
                type=str,
                enum=[
                    "created_at",
                    "-created_at",
                    "updated_at",
                    "-updated_at",
                    "status",
                    "-status",
                    "urgency",
                    "-urgency",
                ],
            ),
        ],
        responses={
            200: IssueListSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    ),
    create=extend_schema(
        summary="Create an issue",
        description="Create a new issue to report a problem with the curriculum.",
        request=IssueCreateSerializer,
        responses={
            201: IssueDetailSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve an issue",
        description="Retrieve details of a specific issue.",
        responses={
            200: IssueDetailSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to access this issue."
            ),
            404: OpenApiResponse(description="Issue not found."),
        },
    ),
    update=extend_schema(
        summary="Update an issue",
        description="Update an issue. Mentors and admins can update any issue, students can only update their own issues.",
        request=IssueUpdateSerializer,
        responses={
            200: IssueDetailSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to update this issue."
            ),
            404: OpenApiResponse(description="Issue not found."),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update an issue",
        description="Partially update an issue. Mentors and admins can update any issue, students can only update their own issues.",
        request=IssueUpdateSerializer,
        responses={
            200: IssueDetailSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to update this issue."
            ),
            404: OpenApiResponse(description="Issue not found."),
        },
    ),
    destroy=extend_schema(
        summary="Delete an issue",
        description="Delete an issue. Only accessible to admins.",
        responses={
            204: OpenApiResponse(description="Issue deleted successfully."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to delete this issue."
            ),
            404: OpenApiResponse(description="Issue not found."),
        },
    ),
)
class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing issues.
    """

    queryset = Issue.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "status",
        "category",
        "urgency",
        "course",
        "project",
        "task",
        "cohort",
        "week_number",
        "reported_by",
        "assigned_to",
    ]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at", "status", "urgency"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        # Students can only see their own issues
        if user.is_student():
            queryset = queryset.filter(reported_by=user)

        # Mentors can see issues from their cohort
        elif user.is_mentor():
            queryset = queryset.filter(cohort=user.cohort)

        # Admins can see all issues (default queryset)

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return IssueCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return IssueUpdateSerializer
        elif self.action == "list":
            return IssueListSerializer
        return IssueDetailSerializer

    def get_permissions(self):
        if self.action == "destroy":
            return [permissions.IsAuthenticated(), IsAdmin()]
        elif self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated(), IsOwnerOrMentorOrAdmin()]
        return [permissions.IsAuthenticated()]

    @extend_schema(
        summary="My issues",
        description="List issues reported by the current user.",
        responses={
            200: IssueListSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    )
    @action(detail=False, methods=["get"])
    def my_issues(self, request):
        """
        List issues reported by the current user.
        """
        queryset = self.get_queryset().filter(reported_by=request.user)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = IssueListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = IssueListSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Assigned issues",
        description="List issues assigned to the current user.",
        responses={
            200: IssueListSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    )
    @action(detail=False, methods=["get"])
    def assigned_to_me(self, request):
        """
        List issues assigned to the current user.
        """
        queryset = self.get_queryset().filter(assigned_to=request.user)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = IssueListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = IssueListSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Add comment to issue",
        description="Add a comment to an issue.",
        request=CommentSerializer,
        responses={
            201: CommentSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            404: OpenApiResponse(description="Issue not found."),
        },
    )
    @action(detail=True, methods=["post"])
    def add_comment(self, request, pk=None):
        """
        Add a comment to an issue.
        """
        issue = self.get_object()
        serializer = CommentSerializer(
            data={"issue": issue.id, "content": request.data.get("content")},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Add feedback to issue",
        description="Add feedback to a resolved issue. Only the reporter can add feedback.",
        request=IssueFeedbackSerializer,
        responses={
            201: IssueFeedbackSerializer,
            400: OpenApiResponse(
                description="Bad request - invalid data or issue not resolved."
            ),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(description="Only the reporter can add feedback."),
            404: OpenApiResponse(description="Issue not found."),
        },
    )
    @action(detail=True, methods=["post"])
    def add_feedback(self, request, pk=None):
        """
        Add feedback to a resolved issue.
        """
        issue = self.get_object()

        # Check if user is the reporter
        if issue.reported_by != request.user:
            return Response(
                {"detail": "Only the reporter can add feedback."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check if issue is resolved
        if issue.status != Issue.RESOLVED:
            return Response(
                {"detail": "Feedback can only be added to resolved issues."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if feedback already exists
        if hasattr(issue, "feedback"):
            return Response(
                {"detail": "Feedback already exists for this issue."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = IssueFeedbackSerializer(
            data={
                "issue": issue.id,
                "rating": request.data.get("rating"),
                "comment": request.data.get("comment", ""),
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    list=extend_schema(
        summary="List comments",
        description="List comments for issues.",
        parameters=[
            OpenApiParameter(
                name="issue",
                description="Filter comments by issue ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="user",
                description="Filter comments by user ID",
                required=False,
                type=int,
            ),
        ],
        responses={
            200: CommentSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    ),
    create=extend_schema(
        summary="Create a comment",
        description="Add a comment to an issue.",
        responses={
            201: CommentSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve a comment",
        description="Retrieve a specific comment.",
        responses={
            200: CommentSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            404: OpenApiResponse(description="Comment not found."),
        },
    ),
    update=extend_schema(
        summary="Update a comment",
        description="Update a comment. Users can only update their own comments, mentors and admins can update any comment.",
        responses={
            200: CommentSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to update this comment."
            ),
            404: OpenApiResponse(description="Comment not found."),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update a comment",
        description="Partially update a comment. Users can only update their own comments, mentors and admins can update any comment.",
        responses={
            200: CommentSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to update this comment."
            ),
            404: OpenApiResponse(description="Comment not found."),
        },
    ),
    destroy=extend_schema(
        summary="Delete a comment",
        description="Delete a comment. Users can only delete their own comments, mentors and admins can delete any comment.",
        responses={
            204: OpenApiResponse(description="Comment deleted successfully."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to delete this comment."
            ),
            404: OpenApiResponse(description="Comment not found."),
        },
    ),
)
class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["issue", "user"]
    ordering_fields = ["created_at"]
    ordering = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        # Students can only see comments on their own issues
        if user.is_student():
            queryset = queryset.filter(issue__reported_by=user)

        # Mentors can see comments from their cohort
        elif user.is_mentor():
            queryset = queryset.filter(issue__cohort=user.cohort)

        # Admins can see all comments (default queryset)

        return queryset

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsOwnerOrMentorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary="List attachments",
        description="List attachments for issues.",
        parameters=[
            OpenApiParameter(
                name="issue",
                description="Filter attachments by issue ID",
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name="uploaded_by",
                description="Filter attachments by uploader user ID",
                required=False,
                type=int,
            ),
        ],
        responses={
            200: AttachmentSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    ),
    create=extend_schema(
        summary="Upload an attachment",
        description="Upload a file attachment for an issue. File size limit is 5MB. Allowed file types include images (jpg, png, gif), documents (pdf, doc, docx, txt), and code files.",
        responses={
            201: AttachmentSerializer,
            400: OpenApiResponse(description="Bad request - invalid data or file."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            413: OpenApiResponse(
                description="File size exceeds the maximum allowed size."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve an attachment",
        description="Retrieve attachment details. The actual file can be downloaded using the file_url property.",
        responses={
            200: AttachmentSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to access this attachment."
            ),
            404: OpenApiResponse(description="Attachment not found."),
        },
    ),
    destroy=extend_schema(
        summary="Delete an attachment",
        description="Delete an attachment. Users can only delete their own attachments, mentors and admins can delete any attachment.",
        responses={
            204: OpenApiResponse(description="Attachment deleted successfully."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to delete this attachment."
            ),
            404: OpenApiResponse(description="Attachment not found."),
        },
    ),
)
class AttachmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing file attachments.
    """

    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["issue", "uploaded_by"]
    ordering_fields = ["uploaded_at", "file_size"]
    ordering = ["-uploaded_at"]
    http_method_names = [
        "get",
        "post",
        "delete",
        "head",
        "options",
    ]  # No update methods
    parser_classes = [MultiPartParser, FormParser]  # For file uploads

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        # Students can only see attachments on their own issues or that they uploaded
        if user.is_student():
            queryset = queryset.filter(Q(issue__reported_by=user) | Q(uploaded_by=user))

        # Mentors can see attachments from their cohort
        elif user.is_mentor():
            queryset = queryset.filter(issue__cohort=user.cohort)

        # Admins can see all attachments (default queryset)

        return queryset

    def get_permissions(self):
        if self.action == "destroy":
            return [permissions.IsAuthenticated(), IsOwnerOrMentorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """Set the current user as uploader and validate issue access"""
        issue_id = self.request.data.get("issue")
        if not issue_id:
            raise serializers.ValidationError({"issue": "Issue ID is required."})

        # Check if issue exists and user has access
        try:
            issue = Issue.objects.get(pk=issue_id)
        except Issue.DoesNotExist:
            raise serializers.ValidationError({"issue": "Issue does not exist."})

        # Check permissions
        user = self.request.user

        # Students can only attach files to their own issues
        if user.is_student() and issue.reported_by != user:
            raise PermissionDenied("You can only attach files to your own issues.")

        # Mentors can only attach files to issues in their cohort
        if user.is_mentor() and issue.cohort != user.cohort:
            raise PermissionDenied(
                "You can only attach files to issues in your cohort."
            )

        serializer.save(uploaded_by=user)

    @extend_schema(
        summary="Download an attachment",
        description="Download the actual file attachment.",
        responses={
            200: OpenApiResponse(description="File will be downloaded."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to access this file."
            ),
            404: OpenApiResponse(description="File not found."),
        },
    )
    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        """
        Download the attachment file directly.
        """
        attachment = self.get_object()

        # Check if file exists
        if not attachment.file or not os.path.exists(attachment.file.path):
            return Response(
                {"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Generate a response with the file
        file_path = attachment.file.path
        file_name = attachment.file_name
        content_type = attachment.content_type or "application/octet-stream"

        response = FileResponse(
            open(file_path, "rb"),
            content_type=content_type,
            as_attachment=True,
            filename=file_name,
        )

        # Add Content-Length header
        response["Content-Length"] = os.path.getsize(file_path)

        return response


@extend_schema_view(
    list=extend_schema(
        summary="List issue templates",
        description="List templates for issue creation.",
        parameters=[
            OpenApiParameter(
                name="category",
                description="Filter templates by category",
                required=False,
                type=str,
                enum=[
                    "checker_error",
                    "unclear_instructions",
                    "typo",
                    "technical_error",
                    "other",
                ],
            ),
            OpenApiParameter(
                name="created_by",
                description="Filter templates by creator user ID",
                required=False,
                type=int,
            ),
        ],
        responses={
            200: IssueTemplateSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    ),
    create=extend_schema(
        summary="Create an issue template",
        description="Create a template for issue creation. Only accessible to mentors and admins.",
        responses={
            201: IssueTemplateSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to create templates."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve an issue template",
        description="Retrieve a specific issue template.",
        responses={
            200: IssueTemplateSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            404: OpenApiResponse(description="Template not found."),
        },
    ),
    update=extend_schema(
        summary="Update an issue template",
        description="Update an issue template. Only the creator, mentors, and admins can update templates.",
        responses={
            200: IssueTemplateSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to update this template."
            ),
            404: OpenApiResponse(description="Template not found."),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update an issue template",
        description="Partially update an issue template. Only the creator, mentors, and admins can update templates.",
        responses={
            200: IssueTemplateSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to update this template."
            ),
            404: OpenApiResponse(description="Template not found."),
        },
    ),
    destroy=extend_schema(
        summary="Delete an issue template",
        description="Delete an issue template. Only the creator, mentors, and admins can delete templates.",
        responses={
            204: OpenApiResponse(description="Template deleted successfully."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to delete this template."
            ),
            404: OpenApiResponse(description="Template not found."),
        },
    ),
)
class IssueTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing issue templates.
    """

    queryset = IssueTemplate.objects.all()
    serializer_class = IssueTemplateSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "created_by"]
    search_fields = ["title", "description_template"]
    ordering_fields = ["title", "category", "created_at"]
    ordering = ["title"]

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsMentorOrAdmin()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsOwnerOrMentorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
