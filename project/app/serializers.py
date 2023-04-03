from app.models import ManufacturingProcess, Operation
from rest_framework import serializers

class ManufacturingProcessSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = ManufacturingProcess
    fields = ['pk', 'name', 'description']

class OperationSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Operation 
    fields = ['pk', 'name', 'description', 'cycle_time', 'process']