from django.urls import path
from . import views 
from search.views import search_results

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('homepage/', views.homepage, name='homepage'), 
    path('autocomplete/',views.autocomplete,name="autocomplete"),
    path("top10/", views.top10_page, name="top10_page"),
    path('library/',views.libraryview,name="libraryview"),
    path('support/', views.support_view, name='support'),
    path('search/', search_results, name='search_results')
]

