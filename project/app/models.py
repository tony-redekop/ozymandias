from django.db import models

# Note: Django automatically creates auto-incrementing primary key field 'pk', but this can be overriden
# The 'blank' argument is validation-related.  If a field has blank=False, the field will be required.
class ManufacturingProcess(models.Model):
  name = models.CharField(blank=True, max_length=255)
  description = models.TextField(blank=True)

# In a one-to-many relationship, a parent entity has multiple child entities.
# Define a ForeignKey field in the child model that references the parent model.
# The related_name is the field in parent model that references child model.
class Operation(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField()
  op_number = models.PositiveIntegerField(unique=True)
  cycle_time = models.DurationField() 
  process = models.ForeignKey(
    ManufacturingProcess,
    on_delete=models.CASCADE,
    related_name='operations'
  )