from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ticker(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/')
    filename = models.CharField(max_length=255)