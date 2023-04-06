from rest_framework import permissions
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

# Set our namespace
app_name = 'app'

schema_view = get_schema_view(
  openapi.Info(
    title="ozymandias.API",
    default_version="v1",
    description="RESTful API for CRUD of manufacturing processes and related entities",
    # terms_of_service="",
    # contact=openapi.Contact(email=""),
    # license=openapi.License(name=""),
  ),
  public=True,
  permission_classes=[permissions.AllowAny],
)

# When using class-based views, as_view() attribute generates callable view function
urlpatterns = [
  path('processes/', views.ManufacturingProcessList.as_view(), name='manufacturingprocess-list'),
  path('processes/<int:pk>/', views.ManufacturingProcessDetail.as_view(), name='manufacturingprocess-detail'),
  path('processes/<int:pk>/operations/', views.OperationList.as_view(), name='operation-list'),
  path('processes/<int:pk>/operations/<int:operation_pk>/', views.OperationDetail.as_view(), name='operation-detail'),
  path('admin/', admin.site.urls),

  # re_path allows us to use regex in our path
  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
  re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]