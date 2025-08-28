from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # API endpoints
    path(
        "api/",
        include(
            [
                # App-specific endpoints
                path("", include("apps.users.urls")),
                path("", include("apps.issues.urls")),
                path("", include("apps.notifications.urls")),
                path("", include("apps.kb.urls")),
                # API schema and documentation
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "docs/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                path(
                    "redoc/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="redoc",
                ),
            ]
        ),
    ),
]

# Add static and media URLs in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
