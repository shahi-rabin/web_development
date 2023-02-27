from django.db import models
from django.contrib.auth.models import User
from main.models import Book

# Create your models here.


class LogisticsData(models.Model):
    studentId =  models.ForeignKey(User, on_delete=models.CASCADE)
    bookName = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowDate = models.DateTimeField(auto_now=True)
    ReturnDate = models.DateField()

    def __str__(self):
        data = str(self.studentId) + " --- " + str(self.ReturnDate) + " , " + str(self.bookName) +  " , "  + str(self.borrowDate) 
        return data

