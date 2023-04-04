from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from . import views

# Set our namespace
app_name = 'app'

# When using class-based views, as_view() attribute generates callable view function
urlpatterns = [
  path('processes/', views.ManufacturingProcessList.as_view(), name='manufacturingprocess-list'),
  path('processes/<int:pk>/', views.ManufacturingProcessDetail.as_view(), name='manufacturingprocess-detail'),
  path('processes/<int:pk>/operations/', views.OperationList.as_view(), name='operation-list'),
  path('processes/<int:pk>/operations/<int:operation_pk>/', views.OperationDetail.as_view(), name='operation-detail'),
  path('admin/', admin.site.urls),
]