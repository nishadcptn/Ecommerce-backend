
from django.urls import path
from Vendor.views import *
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Posts API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)

urlpatterns = [
    path('signup', UserSignUp.as_view(), name='signup'),
    path('org', OrganizationAPI.as_view(), name='upload'),
    path('doc/', schema_view.with_ui('swagger',
                                     cache_timeout=0), name="swagger-schema")
]
