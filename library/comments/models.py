from django.db import models
from books.models import Book
from accounts.models import User
from datetime import datetime
# Create your models here.
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,) 
    pub_date = models.DateTimeField('date published',default=datetime.now(),blank=True)
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=200)

    def to_json(self):
      return { 
        "id" :self.id,    
        "book_title" : self.book.title,
        "user_full_name" :self.user.first_name+" "+self.user.last_name,
        "user_last_name": self.user.last_name,
        "user_email": self.user.email,
       # "review":self.user.review
        "publish_date":self.pub_date,
        "content" : self.content,
        
      }