from django.urls import path
from . import views

urlpatterns = [
    path('recommendations/', views.get_recommendations, name='get_recommendations'),
    path('filtered-books/', views.get_filtered_books, name='get_filtered_books'),
] 