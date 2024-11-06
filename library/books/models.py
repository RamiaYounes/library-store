from django.db import models
from accounts.models import User
from datetime import datetime
from django.db.models import Q,Avg
class Book(models.Model):
   
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
      )
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    year = models.IntegerField()
    price=models.IntegerField(max_length=10,blank=True)
    photos = models.ImageField(upload_to='books/photos/') 
    short_description=models.CharField(max_length=500)
    book_type=models.CharField(max_length=50)
    content=models.FileField(upload_to="books/pdfs/")
    added_date=models.DateTimeField('date published',default=datetime.now(),blank=True)
    rate = models.IntegerField(null=True)
    total_rat= models.IntegerField(default=0)
    num_rat=models.IntegerField(default=0)
    avg_rate=models.FloatField(default=0.0)
  
    def average_rating(self):
   
      return self.total_rat/self.num_rat

    def to_json(self):
      return { 
        "id" :self.id,    
        "title" : self.title,
        "author_full_name" :self.author.first_name+" "+self.author.last_name,
        "author_last_name": self.author.last_name,
        "author_email": self.author.email,
        "short_description":self.short_description,
        "year" : self.year,
        "price":self.price,
        "photos" : self.photos.url,
        "book_type":self.book_type,
        "content":self.content.url,
        "added_date":self.added_date,
        "rate" : self.rate,
        "total_rat": self.total_rat,
        "avg_rate":self.avg_rate
      }

class FavoriteBook(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    book=models.ManyToManyField(Book)
    def to_json(self):
      return { 
        "id" :self.id,    
        "title" : self.book.title,
         "author" :{ 
           "first_name" :self.book.author.first_name,
           "last_name": self.book.author.last_name,
            "email": self.book.author.email,
           "is_staff": self.book.author.is_staff,
           "is_superuser" :self.book.author.is_superuser,
           "is_active": self.book.author.is_active,
         },
         
         "short_description":self.book.short_description,
         "year" : self.book.year,
        "price":self.book.price,
        "photos" : self.book.photos.url,
        "book_type":self.book.book_type,
        "content":self.book.content.url,
        "added_date":self.book.added_date,
        "rate" : self.book.rate,
        "total_rat": self.book.total_rat,}
      
class Purches(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    book=models.ManyToManyField(Book)
    def to_json(self):
      return { 
        "id" :self.id,    
        "title" : self.book.title,
         "author" :{ 
           "first_name" :self.book.author.first_name,
           "last_name": self.book.author.last_name,
            "email": self.book.author.email,

         },
         "short_description":self.book.short_description,
         "year" : self.book.year,
        "price":self.book.price,
        "photos" : self.book.photos.url,
        "book_type":self.book.book_type,
        "content":self.book.content.url,
        "added_date":self.book.added_date,
        "rate" : self.book.rate,
        "total_rat": self.book.total_rat,}
