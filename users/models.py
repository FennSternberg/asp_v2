from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usergroup = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
