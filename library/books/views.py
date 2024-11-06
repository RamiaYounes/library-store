from django.shortcuts import render

# Create your views here.
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from .models import Book,FavoriteBook,Purches
from accounts.models import User
from reviews.models import Review
from django.core import serializers
from django.db.models import Q,Avg
import json
#from .upload_image import upload_image_drive,upload_drive
import datetime

# Create your views here.



@csrf_exempt
def get_book(request,pk):
    info=request.body.decode("utf-8")
    data=json.loads(info)    
    book = Book.objects.get(id=pk) 
    token=data["token"]   
    print(token) 
    if(token):
        #to get the signed in user rate for this book if he has one else it return rate=0
        user=User.objects.get(auth_token=token)
        try:      
            review =Review.objects.get(book=book,user=user)
            book.rate=review.rate 
        except Review.DoesNotExist:
            book.rate=0  
            book.save()
          
    else: 
        book.rate=0
        book.save()
    book_json=book.to_json()
    return JsonResponse(book_json,safe=False)    
                   
    
       
def free_books(request):

    books = Book.objects.filter(price=0) 
    books_json=[book.to_json() for book in books]
            #book_serializer=serializers.serialize('json',books)
    return JsonResponse(books_json,safe=False)     


def all_books(request):
    if request.method=="GET":
        books = Book.objects.all() 
        
           # print("price"+book.price)
        books_json=[book.to_json() for book in books]
        #print("books",books_json)
            #book_serializer=serializers.serialize('json',books)
        return JsonResponse(books_json,safe=False)     
    else:
        return JsonResponse({"message":"method is not allowed"})
@csrf_exempt
def add_rate(request):
    if request.method=="POST":
        data=request.body.decode("utf-8")
        data=json.loads(data)
        print(data)
        book_id=data["book_id"]
        token=data["token"]
        rate=data["rate"]
        try:
            user=User.objects.get(auth_token=token)
            book=Book.objects.get(id=book_id)
            #if the user has added an review befor and want to update it
            try:
                review =Review.objects.get(book=book,user=user)
                book.total_rat=book.total_rat-review.rate      
                review.rate=rate
                
                book.total_rat=book.total_rat+review.rate
                book.avg_rate=book.average_rating()  
            except Review.DoesNotExist:
                review=Review.objects.create(book=book,user=user)
                review.rate=rate   
                book.total_rat= book.total_rat+review.rate
                book.num_rat=book.num_rat+1
                book.avg_rate=book.average_rating()
            book.rate=review.rate
            review.save()
            book.save()
            #book_serializer=serializers.serialize('json',[book,]) 
            #print(book.avg_rate)         
            return JsonResponse({"rate":book.rate},safe=False)
        except Book.DoesNotExist: 
            return JsonResponse({'message': 'The book is not existing'})
    else:
        return JsonResponse({"message":"method is not allowed"})


def rating_books(request):     
    ratingBook=Book.objects.order_by("-avg_rate")     
    books_json=[book.to_json() for book in ratingBook] 
    return JsonResponse(books_json,safe=False)

def latest(request):      
    freash_book=Book.objects.all().order_by("-added_date")    
    books_json=[book.to_json() for book in freash_book] 
        #print(books_json)
    return JsonResponse(books_json,safe=False)
 


###########################
@csrf_exempt
def add_book(request):
    if request.method=="POST":
        user=request.user
        print(user)
        if user.role=="ADMIN":
            title=request.POST.get("title")
            year=request.POST.get("year")
            price=request.POST.get("price")
            book_type=request.POST.get("book_type")
            user_id=request.POST.get("user_id")
            photo=request.FILES['photo']
            content=request.FILES['content']
            print (photo)
            print (content)
            try:         
                author=User.objects.get(id=user_id)
                try:
                    not Book.objects.get(title=title , author=author)  
                    return JsonResponse({'message': 'The book is existing'})
                except Book.DoesNotExist: 
                    book=Book.objects.create(title=title,photos=photo,price=price,author=author,content=content,year=year,book_type=book_type,added_date=datetime.datetime.now())
                    book_serializer=serializers.serialize('json', [ book, ])
                #if not book.clean_fields():
                   # return JsonResponse({'message': 'There is somthing rong'}) 
                    return JsonResponse(book_serializer,safe=False)
            except Book.DoesNotExist: 
                return JsonResponse({'message': 'The author is existing'})
        else:
            return JsonResponse({'message': 'You have not permessions'})
    else:
        return JsonResponse({"message":"method is not allowed"})

def read(request):
    if request.method=="GET":
        data=request.body.decode("utf-8")
        data=json.loads(data)
        book_id=data["book_id"]
        print(book_id)
        try:
            book= Book.objects.get(id=book_id)
            photo=book.photos
            file=book.content  
            #return JsonResponse(photo.url,safe=False)
            return JsonResponse(file.url,headers={"Content_Type":"application/force-download","Content_Disposition":'attachment;filename="{file.name}"'},safe=False)    
            #return JsonResponse(photo.url,safe=False)    
        except Book.DoesNotExist: 
            return JsonResponse({'message': 'The book is not existing'})
    else:
        return JsonResponse({"message":"method is not allowed"})
@csrf_exempt
def search(request):
    info=request.body.decode("utf-8")
    alldata=json.loads(info)
    print(alldata)
    choice=alldata["choice"]
    data=alldata['search']
    if(alldata['token']):
        user=User.objects.get(auth_token=alldata['token'])
        
        if(choice=="favoraite"):
            print("trueeee")
           # favorite =FavoriteBook.objects.get(user=user) 
            books=FavoriteBook.objects.filter(user=user).filter(Q(book__book_type__icontains=data) |Q(book__title__icontains=data)|Q(user__first_name__contains=data))
            print(books)
            if len(books)!=0:
                for boo in books:
                   books_json=[bo.to_json() for bo in boo.book.all()]
                   print(books_json)
                   return JsonResponse(books_json,safe=False)
            else:
               print("llll")
               return JsonResponse({'message': 'The book is not existing'}) 

        elif choice=="purches":
            books=Purches.objects.filter(user=user).filter(Q(book__book_type__icontains=data) |Q(book__title__icontains=data)|Q(user__first_name__contains=data))
            print(books)
            if len(books)!=0:
                for boo in books:
                   books_json=[bo.to_json() for bo in boo.book.all()]
                   print(books_json)
                   return JsonResponse(books_json,safe=False)
            else:
               print("llll")
               return JsonResponse({'message': 'The book is not existing'}) 
    if choice=="free":
            books= Book.objects.filter(Q(price=0) &( Q(book_type__icontains=data) |Q(title__icontains=data)|Q(author__first_name__contains=data)))
            
            if len(books)!=0:
                books_json=[book.to_json() for book in books]
                print(books_json)
                return JsonResponse(books_json,safe=False)
            else:
               print("llll")
               return JsonResponse({'message': 'The book is not existing'}) 
            
       
    elif choice=="all":
            print("1234566")
           
            books=Book.objects.filter(Q(book_type__icontains=data) |Q(title__icontains=data)|Q(author__first_name__contains=data))
            print(books)
            if len(books)!=0:
               books_json=[book.to_json() for book in books]
               print(books_json)
               return JsonResponse(books_json,safe=False)
            else:
               print("llll")
               return JsonResponse({'message': 'The book is not existing'}) 

               
    
@csrf_exempt
def add_to_favoraite(request):
    info=request.body.decode("utf-8")
    data=json.loads(info)
    print(data)
    if(data['token']):
        user=User.objects.get(auth_token=data['token'])
        favorite, created =FavoriteBook.objects.get_or_create(user=user,name="favorite")               
        try:
            bo=Book.objects.get(id=data['book'])
            print (bo)
            favorite.book.add(bo)
            print ("favorite",favorite)
        except Book.DoesNotExist:
            return JsonResponse({'message': 'The book is not existing'})      
            print(favorite.book.all())
        favorite_serializer=[book.to_json() for book in favorite.book.all()]
        print(favorite_serializer)
            #favorite_serializer=serializers.serialize("json",[favorite,])
        return JsonResponse(favorite_serializer,safe=False)
    else:
        return JsonResponse({"detail":"You have to login first"},status=400)
@csrf_exempt
def purches_book(request):
    info=request.body.decode("utf-8")
    data=json.loads(info)
    print(data)
    if(data['token']):
        user=User.objects.get(auth_token=data['token'])
        try:
            purches=Purches.objects.get(user=user)
            print(purches)
            #bo=Book.objects.get(id=book)        
        except Purches.DoesNotExist:
            return JsonResponse({'message': 'You Dont buy any book yet '},status=400)

        purches_serializer=[book.to_json() for book in purches.book.all()]
        print(purches_serializer)
                #favorite_serializer=serializers.serialize("json",[favorite,])
        return JsonResponse(purches_serializer,safe=False)

@csrf_exempt
def favorite(request):
    info=request.body.decode("utf-8")
    data=json.loads(info)
    print(data)
    if(data['token']):
        user=User.objects.get(auth_token=data['token'])
        try:
            favorite=FavoriteBook.objects.get(user=user)
            print(favorite)
            #bo=Book.objects.get(id=book)        
        except FavoriteBook.DoesNotExist:
            return JsonResponse({'message': 'You do not have Favorite books yet, You can add one'},status=400)
        print(favorite.book.all())
                #for book in favorite.book.all():
                   # print(book.id)
        favorite_serializer=[book.to_json() for book in favorite.book.all()]
        print(favorite_serializer)
                #favorite_serializer=serializers.serialize("json",[favorite,])
        return JsonResponse(favorite_serializer,safe=False)
@csrf_exempt
def check_purches(request):
  info=request.body.decode("utf-8")
  data=json.loads(info)
  print(data)
  bo=Book.objects.get(id=data['book'])
  
  if(data['token']):
    user=User.objects.get(auth_token=data['token'])
    try:
        purches=Purches.objects.get(user=user)
        for book in purches.book.all():
            if bo==book:
                return JsonResponse(True,safe=False)
            
        return JsonResponse(False,safe=False)
    except Purches.DoesNotExist:
        return JsonResponse(False,safe=False)
    
@csrf_exempt
def check_favoraite(request):
  info=request.body.decode("utf-8")
  data=json.loads(info)
  print(data)
  bo=Book.objects.get(id=data['book'])
 
  if(data['token']):
    user=User.objects.get(auth_token=data['token'])
    try:
        
        favoraite=FavoriteBook.objects.get(user=user)
        for book in favoraite.book.all():
            print(book)
            if bo==book:
               
                return JsonResponse(True,safe=False)
       
        return JsonResponse(False,safe=False) 
    except FavoriteBook.DoesNotExist:
        return JsonResponse(False,safe=False)
    