from django.db import models

# Create models
# Note: Django automatically creates auto-incrementing primary key
class ManufacturingProcess(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField()

class Operation(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField()
  cycle_time = models.DurationField() 
  process = models.ForeignKey(
    ManufacturingProcess,
    on_delete=models.CASCADE,
  )
