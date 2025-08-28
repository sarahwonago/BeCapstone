from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KnowledgeBaseArticleViewSet

router = DefaultRouter()
router.register(r"kb", KnowledgeBaseArticleViewSet, basename="kb")

urlpatterns = [
    path("", include(router.urls)),
]
