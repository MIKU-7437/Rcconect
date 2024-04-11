from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


schema_view = get_schema_view(
    openapi.Info(
        title="RCconnect API",
        default_version='v0.1.0',
        description="MVP version",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="rconnecct@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    # url=f'{settings.APP_URL}/api/v3/',
    patterns=[path('api/v0.1.0/auth/', include('api.urls')),
              path('api/v0.1.0/users/', include('users.urls')),
              path('api/v0.1.0/events/', include('events.urls')),
              path('api/v0.1.0/tags/', include('tags.urls')),
              ],
    public=True,
)

urlpatterns = [
    path(
        'swagger-ui/',
        TemplateView.as_view(
            template_name='swaggerui/swaggerui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='swagger-ui'),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    path('api/v0.1.0/auth/', include('api.urls'), name='api_auth'),
    path('api/v0.1.0/events/', include('events.urls'), name='api_event'),
    path('api/v0.1.0/tags/', include('tags.urls'), name='api_tags'),
    path('api/v0.1.0/users/', include('users.urls'), name='api_users'),
    path('accounts/', include('allauth.urls')),
    path("admin/", admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]