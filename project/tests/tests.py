from datetime import timedelta
from django.test import TestCase

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from app.models import ManufacturingProcess
from app.models import Operation
from app.serializers import ManufacturingProcessSerializer
from app.serializers import OperationSerializer

# Note: setUp() is run before each test method is run.
# Django flushes test database after each test method completes.
# PostgreSQL doesn't reset auto-incrementing primary key after a flush.
# Test method names must start with 'test' to be found by Django.
class MainTestCase(TestCase):
  def setUp(self):
    # Create model instances and save
    self.manufacturing_process = ManufacturingProcess(
      name="", 
      description=""
    )
    self.manufacturing_process.save()
    self.operation = Operation(
      name="", 
      description="",
      cycle_time=timedelta(seconds=3600),
      process_id=self.manufacturing_process.id  # Foreign key
    )
    self.operation.save()

  def test_models(self):
    try:
      ManufacturingProcess.objects.get(id=1)
      Operation.objects.get(id=1)
    except ManufacturingProcess.DoesNotExist:
      raise ValueError("Invalid primary key for ManufacturingProcess")
    except Operation.DoesNotExist:
      raise ValueError("Invalid primary key for Operation")
 
  def test_serializers(self):
    manufacturing_process_serializer = ManufacturingProcessSerializer(self.manufacturing_process)
    """
    The OperationSerializer requires extra context because we are using hyperlinked relations.  
    The serializer must have access to the request to properly generate fully qualified URLs.  
    """
    factory = APIRequestFactory() # create a test request
    request = factory.get('/')    # create a GET request 
    serializer_context = {'request': Request(request)}
    operation_serializer = OperationSerializer(self.operation, context=serializer_context)