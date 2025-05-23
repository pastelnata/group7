from django.urls import path
from . import views

urlpatterns = [
    path('books/recommendations/', views.get_recommendations, name='get_recommendations'),
    path('homepage/', views.homepage_view, name='homepage'),
]