from django.urls import path,include
from . import views
urlpatterns = [
    #path('', include(router.urls)),

    path('free', views.free_books),
    path('all', views.all_books),
     path('favorite', views.favorite),
     path('purches', views.purches_book),
    
    path('add', views.add_book),
    path('read', views.read),
   
    path('search', views.search),
    path('add/favorite', views.add_to_favoraite),
   
    path('add/rate', views.add_rate),
    path('edit/rate', views.add_rate),
    path('rating', views.rating_books),
    path('latest', views.latest),
    path('<pk>', views.get_book),
    path('check/purches', views.check_purches),
    path('check/favoraite', views.check_favoraite),

    

    ]