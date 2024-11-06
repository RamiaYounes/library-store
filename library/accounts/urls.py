from django.urls import path,include
from . import views

urlpatterns = [
    #path("users",views.users),
    path('signUp/costomer', views.customer_signup,name='customerSignUp'),
    path('signUp/author', views.authorSignUp,name='customerSignUp'),
    path('user/login',views.loginUser,name='userLogin'),
    #path('adminM/login',views.loginAdmin,name='adminLogin'),
    path('logout',views.logoutUser,name='logout'),
    path('get/user', views.get_user),
    path('user', views.get_user_by_token),
    path('check-purches', views.purches),
    path('check-favoraite', views.favoraite),
]
