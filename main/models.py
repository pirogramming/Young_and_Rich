from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Notice(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    context = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_num = models.IntegerField(default=0)