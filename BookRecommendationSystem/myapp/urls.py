from django.urls import path
from . import views 
from search.views import search_results

urlpatterns = [
    path("",views.autocomplete,name="autocomplete"),
    path('autocomplete/',views.autocomplete,name="autocomplete"),
    path('library/',views.libraryview,name="libraryview"),
    path('search/', search_results, name='search_results')
]