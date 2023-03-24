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

  def get_object(self, id):
    try:
      return ManufacturingProcess.objects.get(id=id)
    except ManufacturingProcess.DoesNotExist:
      raise Http404

  def get(self, request, id, format=None):

    manufacturingprocess = self.get_object(id)

    serializer = ManufacturingProcessSerializer(
      manufacturingprocess,
      data=request.data,
      context={'request': request},  # This is required because we use hyper-linked relations
    )
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, id, format=None):
    manufacturingprocess = self.get_object(id)
    serializer = ManufacturingProcessSerializer(manufacturingprocess, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id, format=None):
    manufacturingprocess = self.get_object(id)
    manufacturingprocess.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
