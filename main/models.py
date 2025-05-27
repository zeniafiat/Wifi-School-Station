from django.db import models

# Create your models here.
class DATT(models.Model):
    secure = models.IntegerField(default=0)
    addr = models.IntegerField()
    room = models.IntegerField()
    CO = models.CharField(max_length=8)
    HUM = models.CharField(max_length=3)
    TEMP = models.CharField(max_length=4)
    time = models.TimeField(auto_now=True)
