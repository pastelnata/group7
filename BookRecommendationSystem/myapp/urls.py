from django.urls import include, path
from . import views 

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('search/', include('search.urls')),
    path('recommendation/', include('recommendation.urls')),
    path('autocomplete/',views.autocomplete,name="autocomplete"),
    path('about/', views.about, name='about'), 
    path('library/', views.libraryview, name='libraryview'),
    path('support/', views.support_view, name='support'),
]

