from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserDetails(models.Model):
    studentId = models.CharField(max_length=9)
    batchNo = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

