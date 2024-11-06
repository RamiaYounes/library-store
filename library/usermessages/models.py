"""class Messages(models.Model):
    subject= models.CharField(max_length=20)
    content = models.CharField(max_length=200) 
    pub_date = models.DateTimeField('date published')
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    resever=models.ForeignKey(User,on_delete=models.CASCADE)"""
from django.db import models

from accounts.models import User
# Create your models here.


class UserMessages(models.Model):
    subject= models.CharField(max_length=20)
    content = models.CharField(max_length=200) 
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    