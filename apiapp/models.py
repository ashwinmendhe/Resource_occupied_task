from django.db import models

# Create your models here.
class Resource(models.Model):
    name = models.CharField(max_length=20)
    from_time = models.TimeField()
    to_time = models.TimeField()
    date = models.DateField()
