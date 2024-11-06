from django.contrib import admin
from .models import Book,FavoriteBook,Purches
# Register your models here.
admin.site.register(Book)
admin.site.register(FavoriteBook)
admin.site.register(Purches)