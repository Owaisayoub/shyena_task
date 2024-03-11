from django.db import models

# Create your models here.
class UserProfile(models.Model):
    type = models.CharField(max_length=50)
    frequency = models.CharField(max_length = 20)
    pwr = models.CharField(max_length = 100)
    pw_usec = models.IntegerField()

class LogTable(models.Model):
    type = models.CharField(max_length=50)
    frequency = models.CharField(max_length = 20)
    pwr = models.CharField(max_length = 100)
    pw_usec = models.IntegerField()
    action = models.CharField(max_length=30)
    time_stamp = models.TimeField(auto_now_add = True)

