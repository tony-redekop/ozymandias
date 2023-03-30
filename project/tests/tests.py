# import base64
from datetime import timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command

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

def setup_client(instance):
  # Create test client
  instance.client = APIClient()

  # Create user and and password for test database
  usr = 'testuser'
  pw = 'testpass'
  instance.user = User.objects.create_superuser(
    username=usr,
    password=pw
  )

  # Since we are testing, we force authenticate to avoid complexity
  instance.client.force_authenticate(user=instance.user)

  # We can also use proper authentication shown below
  # Encode the username and password as a byte string
  # credentials = f'{usr}:{pw}'.encode('utf-8')
  # Encode the byte string as a base64-encoded string
  # base64_credentials = base64.b64encode(credentials).decode('utf-8')
  # self.client.credentials(HTTP_AUTHORIZATION='Basic ' + base64_credentials)

# Note: setUp() is run before each test method is run.
# Django flushes test database after each test method completes.
# PostgreSQL doesn't reset auto-incrementing primary key after a flush.
# Test method names must start with 'test' to be found by Django.
class ManufacturingProcessTestCase(TestCase):
  def setUp(self):
    setup_client(self)  # set up test client

  def test_model(self):
    # Create model instance and save to test database
    manufacturing_process = ManufacturingProcess(
      name="Weld Components",
      description="Weld components to forging"
    )
    manufacturing_process.save()

    # Get our instance from test database
    try:
      ManufacturingProcess.objects.get(id=manufacturing_process.id)
    except ManufacturingProcess.DoesNotExist:
      raise ValueError("Invalid primary key for ManufacturingProcess")

  def test_serializer(self):
    manufacturing_process = ManufacturingProcess(
      name="Test name",
      description="Test description",
    )
    expected_data = {
      'id': manufacturing_process.id,
      'name': 'Test name',
      'description': 'Test description',
    }
    process_serializer = ManufacturingProcessSerializer(manufacturing_process)
    self.assertEqual(expected_data, process_serializer.data)

  def test_detail_view(self):
    # Create test data
    data = {'name':'RECIEVE_INSPECT', 'description': 'INSPECT FOR DAMAGE'}

    # Test HTTP POST request
    response = self.client.post('/processes/', data, format='json')
    process_id = response.data['id']
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test HTTP GET request
    response  = self.client.get(f'/processes/{process_id}/')
    self.assertTrue(status.is_success(response.status_code))

class OperationTestCase(TestCase):
  # We use a test fixture to avoid duplication
  # The fixture must be placed in the fixtures directory of one of the INSTALLED_APPS (in settings.py)
  fixtures = ['testdata.json']

  def setUp(self):
    # Call Django management command from our code to load fixture data into test database
    call_command('loaddata', 'testdata.json', verbosity=0)  # equivalent to 'python manage.py loaddata testdata.json'

    manufacturing_process = ManufacturingProcess.objects.get(id=1)

    # Must use _id suffix to assign foreign key field directly, e.g. {foreign_key_name}_id
    # However, this is not good practice; better to utilize model name directly
    self.operation = Operation(
      name="Load Furnace",
      description="Load on a flat plate",
      cycle_time=timedelta(seconds=90),
      # process_id=manufacturing_process  # avoid doing this
      process=manufacturing_process,      # do this instead; see comment above
    )
    self.operation.save()

  def test_model(self):
    try:
      Operation.objects.get(id=self.operation.id)
    except Operation.DoesNotExist:
      raise ValueError("Invalid primary key for Operation")

    self.assertEqual(self.operation.name, "Load Furnace")
    self.assertEqual(self.operation.description, "Load on a flat plate")

  def test_serializer(self):
    """
    OperationSerializer requires extra context because we are using hyperlinked relations.
    The serializer must have access to the request to properly generate fully qualified URLs.
    """
    factory = APIRequestFactory()  # create a test request
    request = factory.get('/')     # create a GET request
    serializer_context = {'request': Request(request)}
    operation_serializer = OperationSerializer(self.operation, context=serializer_context)
    
    expected_data = {
      "name": "Load Furnace",
      "description": "Load on a flat plate",
      "cycle_time": "timedelta(seconds=90)",
      "process": self.operation.id,
    }

  def test_detail_view(self):
    pass