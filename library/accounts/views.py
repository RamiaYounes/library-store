import json
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.core import serializers
from .models import User
from books.models import Book,Purches,FavoriteBook
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_protect,csrf_exempt

# Create your views here.
##############################   Accounts   ############################

@csrf_exempt
def authorSignUp(request):
    if request.method=='POST':
        data= json.loads(request.body)
        first_name=data['first_name']
        last_name=data['last_name']
        password=data['password']
        email=data['email']
        print (first_name)
        try:
           author=User.objects.create_user(first_name=first_name,password=password,last_name=last_name,email=email,role="AUTHOR")
           author_json=author.to_json() 
            #book_serializer=serializers.serialize('json',books)
           return JsonResponse(author_json,safe=False)
        except IntegrityError as e:
            if 'UNIQUE constraint' in e.args[0]:
                 return JsonResponse({'detail':"Email is used,Please try another email"},status=400)

       
    

@csrf_exempt
def customer_signup(request):
        data= json.loads(request.body)
        first_name=data['first_name']
        last_name=data['last_name']
        password=data['password']
        email=data['email']
        try:
           customer=User.objects.create_user(first_name=first_name,password=password,last_name=last_name,email=email,role="CUSTOMER")
           customer_json=customer.to_json() 
           return JsonResponse(customer_json,safe=False)
        except IntegrityError as e:
            if 'UNIQUE constraint' in e.args[0]:
                return JsonResponse({'detail':"Email is used,Please try another email"},status=400)


@csrf_exempt
def loginUser( request):
    if request.method=="POST":
        data= json.loads(request.body)
        email=data["email"]
        #print(email)
        password=data["password"]
        print(password)
        user=authenticate(request,username=email,password=password)
        print(user)
        if not user:     
           return JsonResponse({'detail':"Rong Information"},status=400) 
        login(request,user)
        print("#############")  
        print(request.user)
        token, created = Token.objects.get_or_create(user=user)
        user_json=user.to_json() 
            #book_serializer=serializers.serialize('json',books)
        return JsonResponse({
            'token': token.key,
            'user':user_json,
            'role':user.role
        })

    else:
        return JsonResponse({"message":"method is not allowed"})

#def connect_admin(request):
    

@csrf_exempt
def logoutUser( request):
    if request.method=="POST":
        data=request.body.decode("utf-8")
        data=json.loads(data)
        token=data["token"]
       # user=User.objects.get(auth_token=token)
        print(token)
        #user
        logout(request)
       # token_key=request.auth.key
        token=Token.objects.get(key=token)
        token.delete()   
        return JsonResponse({'detail':"Loged out successfully"} ) 
    else:
        return JsonResponse({"message":"method is not allowed"})

def get_user(request):
    data=request.body.decode("utf-8")
    data=json.loads(data)
    id=data["id"]
    user=User.objects.get(id=id)
    user_serializer=serializers.serialize('json',[user,])
    return JsonResponse(user_serializer,safe=False)

def get_user_by_token(request):
  if request.method=="GET":
   # print("Authorization",request.headers['Authorization'])
    token=request.headers['Authorization']
    print(token)
    user=User.objects.get(auth_token=token)
    
    user_json=user.to_json()
    print(user)
    return JsonResponse(user_json,safe=False)
@csrf_exempt
def purches(request):
    info=request.body.decode("utf-8")
    data=json.loads(info)
    print(data)
    if(data['token']):
        user=User.objects.get(auth_token=data['token'])
        try:
            purches=Purches.objects.get(user=user)
            return JsonResponse(True,safe=False )
        except Purches.DoesNotExist:
            return JsonResponse(False,safe=False)
    else:
         return JsonResponse(False,safe=False)

@csrf_exempt
def favoraite(request):
    info=request.body.decode("utf-8")
    data=json.loads(info)
    print(data)
    if(data['token']):
        user=User.objects.get(auth_token=data['token'])
        try:
            favoraite=FavoriteBook.objects.get(user=user)
            return JsonResponse(True,safe=False )
        except Purches.DoesNotExist:
            return JsonResponse(False,safe=False)
    else:
         return JsonResponse(False,safe=False)


