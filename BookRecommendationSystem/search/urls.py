from django.urls import path
from . import views
from django.http import JsonResponse

urlpatterns = [
    path('', views.search_results, name='bst-search'),
] 