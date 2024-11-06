from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if not email:
            raise ValueError('The Email field must be set')
        if not first_name:
            raise ValueError('The first_name field must be set')
        if not last_name:
            raise ValueError('The last_name field must be set')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, email=email, last_name=last_name ,**extra_fields)
        user.set_password(password)
        print(user.password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,first_name,last_name,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        admin=self.create_user(email= email,password=password,last_name=last_name,first_name=first_name,**extra_fields)
        #admin.set_password(password)
        admin.is_superuser=True
        admin.is_staff=True
       # admin.is_admin=True
        admin.role="ADMIN"
        admin.save(using=self._db)
        return admin

class User(AbstractBaseUser,PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN="ADMIN",'Admin'
        AUTHOR="AUTHOR",'Author'
        CUSTOMER="CUSTOMER",'Customer'
    role=models.CharField(max_length=50,choices=Role.choices,default=Role.CUSTOMER)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50,unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = None
    USERNAME_FIELD="email"
    Email_Field='email'
    REQUIRED_FIELDS=['first_name','last_name','role']
    objects = CustomUserManager()

    def to_json(self):
      return {          
          "first_name" :self.first_name,
          "last_name": self.last_name,
          "email": self.email,
          "role":self.role,
          "id":self.id,
          "password":self.password


      }
    
    
