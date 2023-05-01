from django.shortcuts import render
from django.http import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from app.models import ManufacturingProcess
from app.models import Operation
from app.serializers import ManufacturingProcessSerializer
from app.serializers import OperationSerializer

class RootView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    return Response({"message": "Welcome to ozymandias API"})

# Handles requests that don't specify a specific entity or instance
class ManufacturingProcessList(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request, format=None):
    processes = ManufacturingProcess.objects.all()
    serializer = ManufacturingProcessSerializer(
      processes,
      many=True,
      context={'request': request}
    )
    return Response(serializer.data)

  # @swagger_auto_schema decorator provided by drf-yasg defines additional request body parameters
  @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, max_length=255),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            # Add more fields as needed
        },
        required=['name', 'description']  # Specify required fields
    ),
    responses={201: 'Created', 400: 'Bad Request'}
  )
  # In RESTful design, HTTP POST is non-idempotent and always creates a new resource
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
      # If using a PUT request, we create a resource if it doesn't exist
      if self.request.method == 'PUT':
        return
      # If not PUT, we raise a 404
      raise Http404

  def get(self, request, pk, format=None):
    manufacturingprocess = self.get_object(pk)
    serializer = ManufacturingProcessSerializer(
      manufacturingprocess,
      context={'request': request},  # This is required because we use hyper-linked relations
    )
    return Response(serializer.data)

  # @swagger_auto_schema decorator provided by drf-yasg defines additional request body parameters
  @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, max_length=255),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            # Add more fields as needed
        },
        required=['name', 'description']  # Specify required fields
    ),
    responses={200: 'OK', 201: 'Created', 400: 'Bad Request'}
  )
  # HTTP PUT is idempotent; it will create a resource if it doesn't exist or update an existing resource
  # If resource with given pk does not exist, we create one
  def put(self, request, pk, format=None):
    try:
      manufacturingprocess = self.get_object(pk)
      serializer = ManufacturingProcessSerializer(
        manufacturingprocess,
        data=request.data,
        context={'request': request},
      )
    except manufacturingprocess.DoesNotExist:
      serializer = ManufacturingProcessSerializer(
        data=request.data,
        context={'request': request},
      )

    if serializer.is_valid():  # must validate since we are creating / updating objects
      serializer.save()
      if manufacturingprocess:
        # If updated
        return Response(serializer.data, status=status.HTTP_200_OK)
      else:
        # If created
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    manufacturingprocess = self.get_object(pk)
    manufacturingprocess.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Handles requests that don't specify a specific object or instance
class OperationList(APIView):

  permission_classes = [permissions.IsAuthenticated]
  # authentication_classes = [BasicAuthentication]

  # pk is primary key of parent; operation_pk is primary key of child
  def get_parent_object(self, pk):
    try:
      return ManufacturingProcess.objects.get(pk=pk)
    except ManufacturingProcess.DoesNotExist:
      raise Http404

  def get(self, request, pk, format=None):
    manufacturing_process = self.get_parent_object(pk)
    operations = manufacturing_process.operations.all()
    serializer = OperationSerializer(
      operations,
      many=True,
      context={'request': request},
    )
    return Response(serializer.data)

# Handles requests that specify a specific object or instance
class OperationDetail(APIView):

  permission_classes = [permissions.IsAuthenticated]
  # authentication_classes = [BasicAuthentication]
  '''
  `pk` is primary key of related model; `op_number` is non-primary-key identifer
  Exposing a URL with op_number instead of a primary key is more user-friendly
  and integrates better with our business logic
  '''
  def get_object(self, pk, op_number):
    try:
      # `process_id` parameter points to primary key of related entity
      # `process` is the name of ForeignKey field in the model and appending `_id` is Django / DRF specific behavior
      return Operation.objects.get(process_id=pk, op_number=op_number)
    except Operation.DoesNotExist:
      raise Http404

  def get(self, request, pk, op_number):
    operation = self.get_object(pk, op_number)
    serializer = OperationSerializer(operation,
      context={'request': request},  # context required when using hyper-linked relations
    )
    return Response(serializer.data)

  @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, max_length=255),
            'op_number': openapi.Schema(type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT32),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'cycle_time': openapi.Schema(type=openapi.TYPE_STRING),
            'process': openapi.Schema(type=openapi.TYPE_STRING),
            # Add more fields as needed
        },
        required=['name', 'op_number', 'description', 'cycle_time', 'process']  # Specify required fields
    ),
    responses={200: 'OK', 201: 'Created', 400: 'Bad Request'}
  )
  def put(self, request, pk, op_number, format=None):
    try:
      operation = self.get_object(pk, op_number)
      serializer = OperationSerializer(
        operation,
        data=request.data,
        context={'request': request},
      )
    except operation.DoesNotExist:
      serializer = OperationSerializer(
        data=request.data,
        context={'request': request},
      )

    if serializer.is_valid():  # must validate since we are creating / updating objects
      serializer.save()
      if operation:
        # If updated
        return Response(serializer.data, status=status.HTTP_200_OK)
      else:
        # If created
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, op_number, format=None):
    operation = self.get_object(pk, op_number)
    operation.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)