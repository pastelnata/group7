from django.urls import path
from . import views
from django.http import JsonResponse

urlpatterns = [
    path('', views.search_results, name='search_results'),
    path('top10/', views.top10_results, name='top10_page'),
    path('books/<int:book_id>/recommendations/', views.recommended_books, name='recommended_books'),
] 