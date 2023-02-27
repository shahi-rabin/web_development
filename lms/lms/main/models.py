from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    bookId =   models.AutoField(primary_key=True)
    bookName = models.CharField(max_length=300)
    authorName = models.CharField(max_length=300)

    def __str__(self):
        return self.bookName
