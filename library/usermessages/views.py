from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from accounts.models import User
from django.core import serializers
import json
from .models import UserMessages
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
@csrf_exempt
def add_message(request):
   
        info=request.body.decode("utf-8")
        data=json.loads(info) 
        print(data)    
        token=data['token']
        mess=data["mess"]
        if(data['token']):
           user=User.objects.get(auth_token=data['token'])
           content=mess["content"]
           subject=mess["subject"]
           mes= UserMessages()
           mes.content = content
           mes.subject = subject
           mes.sender = user
           mes.save() 
           return JsonResponse({"message":"Thanks For Your Message,Our Response Will Be ASAP "})


