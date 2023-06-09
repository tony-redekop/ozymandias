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
from rest_framework.reverse import reverse
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

class RootViewTestCase(TestCase):
  def setUp(self):
    setup_client(self)  # set up test client
  
  def test_root_view(self):
    # Test HTTP GET request
    url = reverse('app:root-view')
    response  = self.client.get(url)
    self.assertTrue(status.is_success(response.status_code))

# Note: setUp() is run before each test method is run.
# Django flushes test database after each test method completes.
# PostgreSQL doesn't reset auto-incrementing primary key after a flush.
# Test method names must start with 'test' to be found by Django.
class ManufacturingProcessTestCase(TestCase):
  def setUp(self):
    setup_client(self)  # set up test client
    # self.client.get('/invalid-url/')  # clear URL pattern cache

  def test_model(self):
    # Create model instance and save to test database
    manufacturing_process = ManufacturingProcess(
      name="Weld Components",
      description="Weld components to forging"
    )
    manufacturing_process.save()

    # Get our instance from test database
    try:
      ManufacturingProcess.objects.get(pk=manufacturing_process.pk)
    except ManufacturingProcess.DoesNotExist:
      raise ValueError("Invalid primary key for ManufacturingProcess")

  def test_serializer(self):
    manufacturing_process = ManufacturingProcess(
      name="Test name",
      description="Test description",
    )
    expected_data = {
      'pk': manufacturing_process.pk,
      'name': 'Test name',
      'description': 'Test description',
      'operations': []
    }
    process_serializer = ManufacturingProcessSerializer(manufacturing_process)
    self.assertEqual(expected_data, process_serializer.data)

  def test_views(self):
    # Create test data
    # data = {'pk': 1, 'name':'RECIEVE_INSPECT', 'description': 'INSPECT FOR DAMAGE'}
    data = {'name':'RECIEVE_INSPECT', 'description': 'INSPECT FOR DAMAGE'}

    # Test list-view POST request
    response = self.client.post('/processes/', data, format='json')
    process_pk = response.data['pk']
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test list-view GET request
    response = self.client.get('/processes/')
    self.assertTrue(status.is_success(response.status_code))
    
    # Test detail-view GET request
    response = self.client.get(f'/processes/{process_pk}/')
    self.assertTrue(status.is_success(response.status_code))

    # Test detail-view DELETE request
    response = self.client.delete(f'/processes/{process_pk}/')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test detail-view PUT request
    # Our implementation of PUT is idempotent in conformance to RESTful design principles
    # But if the resource with given pk does not exist, a new resource is created
    url = reverse('app:manufacturingprocess-detail',
      args=[process_pk]
    )
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class OperationTestCase(TestCase):
  # We use a test fixture to avoid duplication
  # The fixture must be placed in the fixtures directory of one of the INSTALLED_APPS (in settings.py)
  fixtures = ['testdata.json']

  def setUp(self):
    setup_client(self)

    # Call Django management command from our code to load fixture data into test database
    call_command('loaddata', 'testdata.json', verbosity=0)  # equivalent to 'python manage.py loaddata testdata.json'

    self.manufacturing_process = ManufacturingProcess.objects.get(pk=1)

    # Define URLs for related fields
    self.url = reverse('app:manufacturingprocess-detail',
      args=[self.manufacturing_process.pk]
    )

    self.operation = Operation(
      name="Load Furnace",
      description="Load on a flat plate",
      op_number=10,
      cycle_time=timedelta(seconds=90),
      process=self.manufacturing_process,  # note: using instance, not instance.pk 
    )
    self.operation.save()

  def test_model(self):
    try:
      Operation.objects.get(pk=self.operation.pk)
    except Operation.DoesNotExist:
      raise ValueError("Invalid primary key for Operation")

    self.assertEqual(self.operation.name, "Load Furnace")
    self.assertEqual(self.operation.description, "Load on a flat plate")

  def test_serializer(self):
    """
    OperationSerializer requires extra context because we are using hyperlinked relations.
    With hyperlinked relations, we relate models with a URL and not a pk.
    The serializer must have access to the request to properly generate fully qualified URLs.
    """
    factory = APIRequestFactory()  # create a test request
    request = factory.get(f'operations/{self.operation.pk}/')     # create a GET request
    serializer_context = {'request': Request(request)}
    operation_serializer = OperationSerializer(self.operation, context=serializer_context)

    # Must add namespace 'app:' before the URL pattern name
    url = reverse('app:manufacturingprocess-detail',
      args=[self.manufacturing_process.pk]
    )

    # timedelta() returns string with form 'H:MM:SS'
    # operation_serializer.data returns string with form 'HH:MM:SS'
    # Therefore we format output of timedelta to include a leading '0' digit
    # This solution does not cover all edge cases; need to refactor.
    expected_data = {
      "pk": self.operation.pk,
      "name": "Load Furnace",
      "op_number": 10,
      "description": "Load on a flat plate",
      "cycle_time": f"0{timedelta(seconds=90)}",
      "process": f"http://testserver{url}",
    }
    self.assertEqual(operation_serializer.data, expected_data)

  def test_views(self):
    # Create test data
    op_number = 10    
    testdata = {
      "pk": self.operation.pk,
      "name": "Load Furnace",
      "op_number": op_number,
      "description": "Load on a flat plate",
      "cycle_time": f"0{timedelta(seconds=90)}",
      "process": f"http://testserver{self.url}",
    }

    # Test detail-view PUT request
    url = reverse('app:operation-detail',
      args=[self.manufacturing_process.pk, op_number]
    )
    response = self.client.put(url, testdata, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Test list-view GET request
    url = reverse('app:operation-list',
      args=[self.manufacturing_process.pk]
    )
    response = self.client.get(url)

    # Test detail-view GET request
    url = reverse('app:operation-detail',
      args=[self.manufacturing_process.pk, op_number]
    )
    response = self.client.get(url)
    self.assertTrue(status.is_success(response.status_code))

    # Test detail-view DELETE request
    response = self.client.delete(url)
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)