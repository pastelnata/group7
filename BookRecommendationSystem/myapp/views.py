import json
from django.db.models.functions import Random
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .utils import get_sorted_books
from .models import Book 

#from .models import Library


def book_list_example(request):
    """
    Example function showing how to use the sorting in a view
    without modifying your existing templates
    """
    # Get sort parameters from request (or use defaults)
    sort_key = request.GET.get('sort', 'stars')
    order = request.GET.get('order', 'desc')
    
    # Validate sort key against available fields
    valid_sort_keys = ['stars', 'reviews', 'price', 'published_date']
    if sort_key not in valid_sort_keys:
        sort_key = 'stars'
    
    # Get sorted books using the merge sort algorithm
    sorted_books = get_sorted_books(sort_key, order)
    
    # Add to context for your existing templates
    context = {
        'books': sorted_books,
        # other context variables your template might need
    }


def autocomplete(request):
    """     when LIbrary is name of the database

task1. create database
task2 implement autosuggestions not only for title but also for author

    if 'term' in request.GET:
        qs = Library.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)

        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
        """
    return render(request,"home.html")