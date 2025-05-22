from django.urls import include, path
from . import views 

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('homepage/', views.homepage, name='homepage'), 
    path('autocomplete/',views.autocomplete,name="autocomplete"),
    path('about/', views.about, name='about'), 
    path('library/', views.libraryview, name='libraryview'),
    path('support/', views.support_view, name='support'),
    path('books/recommendations/', views.get_recommendations, name='get_recommendations'),
    path('', include('search.urls'))
]

