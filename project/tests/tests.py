# import base64
from datetime import timedelta

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework import status

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

    # Create test client
    self.client = APIClient()

    usr = 'testuser'
    pw = 'testpass'

    self.user = User.objects.create_superuser(
      username=usr,
      password=pw
    )

    self.client.force_authenticate(user=self.user)

    # # Encode the username and password as a byte string
    # credentials = f'{usr}:{pw}'.encode('utf-8')

    # # Encode the byte string as a base64-encoded string
    # base64_credentials = base64.b64encode(credentials).decode('utf-8')

    # self.client.credentials(HTTP_AUTHORIZATION='Basic ' + base64_credentials)

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

  def test_process_detail_view(self):
    # Create test data
    data = {'name':'RECIEVE_INSPECT', 'description': 'INSPECT FOR DAMAGE'}

    # Test HTTP POST request 
    response = self.client.post('/processes/', data, format='json')
    process_id = response.data['id']
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test HTTP GET request
    response  = self.client.get(f'/processes/{process_id}/')
    self.assertTrue(status.is_success(response.status_code))