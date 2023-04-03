from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from . import views

# When using class-based views, as_view() attribute generates callable view function
urlpatterns = [
  path('processes/', views.ManufacturingProcessList.as_view(), name='manufacturingprocess-list'),
  path('processes/<int:pk>/', views.ManufacturingProcessDetail.as_view(), name='manufacturingprocess-detail'),
  path('admin/', admin.site.urls),
]