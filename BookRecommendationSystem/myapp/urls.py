from django.urls import include, path
from . import views 

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('homepage/', views.homepage, name='homepage'), 
    path('autocomplete/',views.autocomplete,name="autocomplete"),
    path('library/', views.libraryview, name='library'),
    path('support/', views.support_view, name='support'),
    path('', include('search.urls'))
]

