from django.contrib import admin
from django.urls import include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Quizzes API",
        default_version="v1",
        description="API for quizzes",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(r"^api/v1/polls/", include("polls.urls")),
    re_path(r"^api/v1/swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^api/v1/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^api/v1/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
