from django.shortcuts import render
from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import ManufacturingProcess
from app.models import Operation
from app.serializers import ManufacturingProcessSerializer
from app.serializers import OperationSerializer

# Handles requests that don't specify a specific object or instance
class ManufacturingProcessList(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request, format=None):
    processes = ManufacturingProcess.objects.all()
    serializer = ManufacturingProcessSerializer(processes, many=True)
    return Response(serializer.data)

  def post(self, request, format=None):
    serializer = ManufacturingProcessSerializer(
      data=request.data,
      context={'request': request}
    )
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Handles requests that specify a specific object or instance
class ManufacturingProcessDetail(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get_object(self, pk):
    try:
      return ManufacturingProcess.objects.get(pk=pk)
    except ManufacturingProcess.DoesNotExist:
      raise Http404

  def get(self, request, pk, format=None):
    manufacturingprocess = self.get_object(pk)
    serializer = ManufacturingProcessSerializer(
      manufacturingprocess,
      context={'request': request},  # This is required because we use hyper-linked relations
    )
    return Response(serializer.data)

  def put(self, request, pk, format=None):
    manufacturingprocess = self.get_object(pk)
    serializer = ManufacturingProcessSerializer(manufacturingprocess, data=request.data)
    if serializer.is_valid():  # must validate since we are creating / updating objects
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    manufacturingprocess = self.get_object(pk)
    manufacturingprocess.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Handles requests that don't specify a specific object or instance
class OperationList(APIView):

  permission_classes = [permissions.IsAuthenticated]
  # authentication_classes = [BasicAuthentication]

  def get(self, request, format=None):
    operations = Operation.objects.all()
    serializer = OperationSerializer(operations, many=True)
    return Response(serializer.data)

  def post(self, request, pk, format=None):
    serializer = OperationSerializer(data=request.data,
      context={'request': request} # This is required because we use hyper-linked relations
    )
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Handles requests that specify a specific object or instance
class OperationDetail(APIView):

  permission_classes = [permissions.IsAuthenticated]
  # authentication_classes = [BasicAuthentication]

  # pk is primary key of related model; operation_pk is primary key of object we want
  def get_object(self, pk, operation_pk):
    try:
      return Operation.objects.get(pk=operation_pk, process_id=pk)
    except Operation.DoesNotExist:
      raise Http404

  def get(self, request, pk, operation_pk):
    operation = self.get_object(pk, operation_pk)
    serializer = OperationSerializer(operation,
      context={'request': request},  # context required when using hyper-linked relations
    )
    return Response(serializer.data)

  def put(self, request, pk, format=None):
    operation = self.get_object(pk)
    serializer = OperationSerializer(operation, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    operation = self.get_object(pk)
    operation.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)