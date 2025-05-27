from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True)
    sensor_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username