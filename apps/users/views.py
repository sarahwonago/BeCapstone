from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes

from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
)
from .permissions import IsAdmin, IsMentorOrAdmin, IsOwnerOrMentorOrAdmin
from .token import CustomTokenObtainPairView

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="List all users. Only accessible to mentors and admins.",
        responses={
            200: UserSerializer(many=True),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
        },
    ),
    create=extend_schema(
        summary="Create a new user",
        description="Create a new user account. Only accessible to admins.",
        responses={
            201: UserDetailSerializer,
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
        summary="Retrieve a user",
        description="Retrieve a specific user by ID. Users can retrieve their own details, mentors and admins can retrieve any user.",
        responses={
            200: UserDetailSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="User not found."),
        },
    ),
    update=extend_schema(
        summary="Update a user",
        description="Update a user's information. Users can update their own details, admins can update any user.",
        responses={
            200: UserDetailSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="User not found."),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update a user",
        description="Partially update a user's information. Users can update their own details, admins can update any user.",
        responses={
            200: UserDetailSerializer,
            400: OpenApiResponse(description="Bad request - invalid data."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="User not found."),
        },
    ),
    destroy=extend_schema(
        summary="Delete a user",
        description="Delete a user. Only accessible to admins.",
        responses={
            204: OpenApiResponse(description="User deleted successfully."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
            403: OpenApiResponse(
                description="You do not have permission to perform this action."
            ),
            404: OpenApiResponse(description="User not found."),
        },
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    """

    queryset = User.objects.all().order_by("-date_joined")

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        elif self.action == "retrieve" or self.detail:
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsAdmin()]
        elif self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated(), IsOwnerOrMentorOrAdmin()]
        elif self.action == "destroy":
            return [permissions.IsAuthenticated(), IsAdmin()]
        elif self.action == "list":
            return [permissions.IsAuthenticated(), IsMentorOrAdmin()]
        elif self.action == "retrieve":
            return [permissions.IsAuthenticated(), IsOwnerOrMentorOrAdmin()]
        return [permissions.IsAuthenticated()]

    @extend_schema(
        summary="Change user password",
        description="Change the authenticated user's password.",
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password changed successfully."),
            400: OpenApiResponse(description="Bad request - invalid password."),
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    )
    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def change_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"detail": "Password changed successfully."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Get current user",
        description="Get the authenticated user's details.",
        responses={
            200: UserDetailSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    )
    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)


@extend_schema(
    summary="Register a new user",
    description="Register a new user account.",
    request=UserCreateSerializer,
    responses={
        201: UserDetailSerializer,
        400: OpenApiResponse(description="Bad request - invalid data."),
    },
    tags=["authentication"],
)
class RegisterView(generics.CreateAPIView):
    """
    Register a new user.
    """

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens for the user
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserDetailSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    summary="Login to get access token",
    description="Login with username and password to get access and refresh tokens.",
    tags=["authentication"],
)
class LoginView(CustomTokenObtainPairView):
    """
    Login view to obtain access and refresh tokens.
    """

    pass


@extend_schema(
    summary="Refresh access token",
    description="Refresh the access token using a valid refresh token.",
    tags=["authentication"],
)
class RefreshTokenView(TokenRefreshView):
    """
    Refresh token view to obtain a new access token.
    """

    pass
