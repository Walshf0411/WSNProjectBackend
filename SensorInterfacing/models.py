from django.db import models

# Create your models here.
class Temprature_Record(models.Model):
    node = models.CharField(max_length=10)
    temprature = models.FloatField()
    date_received = models.DateTimeField(auto_now=True)

class Image(models.Model):
    image = models.FileField()