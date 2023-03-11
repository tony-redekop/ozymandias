from app.models import ManufacturingProcess, Operation
from rest_framework import serializers

class ManufacturingProcessSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = ManufacturingProcess
    fields = ['id', 'name', 'description']

class OperationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Operation 
    fields = ['id', 'name', 'description', 'cycle_time', 'process']


