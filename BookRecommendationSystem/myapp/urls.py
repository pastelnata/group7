from django.urls import path
from . import views 

urlpatterns = [
    path('', views.homepage, name='homepage'), 
    path("",views.autocomplete,name="autocomplete"),
    path('library',views.libraryview,name="libraryview")

]

