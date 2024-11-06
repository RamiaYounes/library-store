from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from books.models import Book,FavoriteBook
from reviews.models import Review
from accounts.models import User
from django.core import serializers
from django.db.models import Q
import json
from django.shortcuts import get_object_or_404
from .models import Comment
import datetime
@csrf_exempt
def add_comment(request):
    if request.method=="POST":
        info=request.body.decode("utf-8")
        data=json.loads(info)
        book_id=data["book_id"]
        token=data["token"]
        book = get_object_or_404(Book, pk=book_id)
        content = data['content']
        user= User.objects.get(auth_token=token)
        comment = Comment()
        comment.book = book
        comment.user = user
        comment.pub_date = datetime.datetime.now()
        comment.content=content
        comment.save()
        comment_json=comment.to_json()
        return JsonResponse(comment_json,safe=False)
    else:
        return JsonResponse({"message":"method is not allowed"})
@csrf_exempt
def all_comments(request):
    
        info=request.body.decode("utf-8")
        data=json.loads(info)
        book_id=data["book_id"]
        book=Book.objects.get(id=book_id)
        comments = Comment.objects.filter(book=book) 
        #comment_json=[comment.to_json() for comment in comments] 
        #print(comment_json)
        comment_json=[]
        for comment in comments:
            print(comment.user)
            comm=comment.to_json()
            try:
                review=Review.objects.get(user=comment.user,book=book)
                comm["rate"]=review.rate
            except Review.DoesNotExist:        
                comm["rate"]=0
               
            comment_json.append(comm)
        
        return JsonResponse(comment_json,safe=False)
     



