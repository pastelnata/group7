import json

from django.db.models.functions import Random

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from books.models import Book
from search.views import search_books
# Create your views here.

def libraryview(request):
    event_list=Book.objects.all()
    # random books since loading whole database makes the system loads for at least 5 min or it is breaking 
    random_books = event_list.order_by(Random())[:10]  
    return render(request, "libraryview.html", {'event_list': random_books})  

def autocomplete(request):
    if 'term' in request.GET:
        qs = Book.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)

        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    return render(request,"home.html")

def top10_page(request):
    # dummy data
    top10s = {
        "Top 10 fiction": [f"Book {i}" for i in range(1, 11)],
        "Top 10 non-fiction": [f"Book {i}" for i in range(1, 11)],
        "Top 10 science": [f"Book {i}" for i in range(1, 11)],
        "Top 10 history": [f"Book {i}" for i in range(1, 11)],
        "Top 10 fantasy": [f"Book {i}" for i in range(1, 11)],
        "Top 10 biography": [f"Book {i}" for i in range(1, 11)],
        "Top 10 mystery": [f"Book {i}" for i in range(1, 11)],
        "Top 10 romance": [f"Book {i}" for i in range(1, 11)],
    }
    return render(request,"top10.html", {"top10s": top10s})

def homepage(request):
    return render(request, "homepage.html")
