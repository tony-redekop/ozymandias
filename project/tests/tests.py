from django.test import TestCase
from app.models import ManufacturingProcess
from app.models import Operation

class ManufacturingProcessTestCase(TestCase):
  def setup(self):
    ManufacturingProcess.objects.create(name="Recieving Inspection", description="Visual inspection for obvious damage")
  
  # Define test methods 
  # Note: Test method names must start with 'test'
  def test1(self):
    print("test1 passed")