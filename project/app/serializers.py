from app.models import ManufacturingProcess, Operation
from rest_framework import serializers

class ManufacturingProcessSerializer(serializers.HyperlinkedModelSerializer):
  operations = serializers.HyperlinkedRelatedField(
    many=True,
    read_only=True,
    view_name='app:operation-detail'
  )
  class Meta:
    model = ManufacturingProcess
    fields = ['pk', 'name', 'description', 'operations']

class OperationSerializer(serializers.HyperlinkedModelSerializer):
  # We must include a HyperlinkedRelatedField since we are using hyperlinked relations with a namespace
  # Must also include a queryset or set read_only=`True`
  process = serializers.HyperlinkedRelatedField(
    many=False, 
    queryset=ManufacturingProcess.objects.all(),
    view_name='app:manufacturingprocess-detail',
  )
  class Meta:
    model = Operation 
    fields = ['pk', 'name', 'description', 'cycle_time', 'process']