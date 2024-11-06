from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from books.models import Book,FavoriteBook
from accounts.models import User
from django.core import serializers
from django.db.models import Q,Avg
import json

# Create your views here.
@csrf_exempt
def add_rate(request):
    if request.method=="POST":
        data=request.body.decode("utf-8")
        data=json.loads(data)
        book_id=data["book_id"]
        try:
            book= Book.objects.get(id=book_id)
            book.rate= data["rate"]
            book.total_rat= book.total_rat+book.rate
            book.save()
            book_serializer=serializers.serialize('json',[book,])          
            return JsonResponse({'total_rat': book.total_rat,"book":book_serializer},safe=False)
        except Book.DoesNotExist: 
            return JsonResponse({'message': 'The book is not existing'})
    else:
        return JsonResponse({"message":"method is not allowed"})

def rating_books(request):
    if request.method=="GET":
        
        ratingBook=Book.objects.annotate(avg_rating=Avg("review_set_rate")).order_by("-avg_rating")
        print(ratingBook[1].avg_rating)
        books_json=[book.to_json() for book in ratingBook]
        return JsonResponse(books_json,safe=False)
    else:
        return JsonResponse({"message":"method is not allowed"}) 