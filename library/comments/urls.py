from django.urls import path,include
from . import views

urlpatterns = [
    path("all",views.all_comments),
    path("add",views.add_comment),

]
