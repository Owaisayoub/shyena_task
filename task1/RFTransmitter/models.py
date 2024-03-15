from django.db import models

# Create your models here.
class ConfigTable(models.Model):
    type = models.CharField(max_length=50)
    frequency = models.CharField(max_length = 20)
    prf = models.IntegerField( null = True)
    pw = models.IntegerField( null = True)
    status = models.CharField(max_length = 20, null = True)
    pid = models.IntegerField( null = True )

class LogTable(models.Model):
    type = models.CharField(max_length=50)
    frequency = models.CharField(max_length = 20)
    prf = models.IntegerField(null = True)
    pw = models.IntegerField(null = True)
    action = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now=True)
    

