from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CourseViewSet,
    ProjectViewSet,
    TaskViewSet,
    IssueViewSet,
    CommentViewSet,
    AttachmentViewSet,
    IssueTemplateViewSet,
)

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"issues", IssueViewSet, basename="issue")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"attachments", AttachmentViewSet, basename="attachment")
router.register(r"templates", IssueTemplateViewSet, basename="issue-template")

urlpatterns = [
    path("", include(router.urls)),
]
