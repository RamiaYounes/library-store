from django.db import models
from accounts.models import User
from books.models import Book
# Create your models here.
class Card(models.Model):    
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    balance = models.IntegerField(max_length=50,null=True)