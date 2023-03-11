from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from app.models import ManufacturingProcess
from app.models import Operation
from app.serializers import ManufacturingProcessSerializer
from app.serializers import OperationSerializer

class ManufacturingProcessViewSet(viewsets.ModelViewSet):
  # API endpoint that allows manufacturing processes to be viewed or edited
  queryset = ManufacturingProcess.objects.all()
  serializer_class = ManufacturingProcessSerializer
  permission_classes = [permissions.IsAuthenticated]

class OperationViewSet(viewsets.ModelViewSet):
  # API endpoint that allows manufacturing processes to be viewed or edited
  queryset = Operation.objects.all()
  serializer_class = OperationSerializer
  permission_classes = [permissions.IsAuthenticated]