from django.db import models
from accounts.models import User
from books.models import Book

# Create your models here.
class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
      )
    rate = models.IntegerField(choices=RATING_CHOICES,default=0)

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name="reviews")

    
 