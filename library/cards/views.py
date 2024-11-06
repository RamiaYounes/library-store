from django.shortcuts import render
from .models import Card
from accounts.models import User
from books.models import Book,Purches
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import json
# Create your views here.
@csrf_exempt
def buy(request,pk):
    info=request.body.decode("utf-8")
    data=json.loads(info)    
    book = Book.objects.get(id=pk) 
    print(book)
    token=data["token"]   
    print(token) 
    if(token):
        user=User.objects.get(auth_token=token)
        try:
            purches=Purches.objects.get(user=user)
      
            try:
                    card=Card.objects.get(user=user)
                    if(card.balance >=book.price):
                      card.balance=card.balance-book.price
                      card.save()   
                      purches.book.add(book)
              
                      purches_serializer=[ book.to_json() for book in purches.book.all() ]
                      print(purches)
        
                      return JsonResponse(purches_serializer,safe=False)
                    else: 
                       return JsonResponse({"mess":"You dont have enough money"},status=400)
            except Card.DoesNotExist: 
                    return JsonResponse({'mess': 'You have to create account and add money'},status=400)

        except Purches.DoesNotExist:
         try:
              card=Card.objects.get(user=user)
              if(card.balance >=book.price):
                 card.balance=card.balance-book.price
                 card.save()
                 purches=Purches.objects.create(user=user)   
                 purches.book.add(book)
               
                 purches_serializer=[ book.to_json() for book in purches.book.all() ]
                 print(purches)
        
                 return JsonResponse(purches_serializer,safe=False)
              else: 
                 return JsonResponse({"mess":"You dont have enough money"},status=400)
         except Card.DoesNotExist: 
            return JsonResponse({'mess': 'You have to create account and add money'},status=400)
    else:    
       return JsonResponse({"detail":"You have to login first"},status=400) 
    