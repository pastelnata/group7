import json

from django.db.models.functions import Random

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from books.models import Book
# Create your views here.

def libraryview(request):
    event_list=Book.objects.all()
    # random books since loading whole database makes the system loads for at least 5 min or it is breaking 
    random_books = event_list.order_by(Random())[:10]  
    return render(request, "libraryview.html", {'event_list': random_books})  

def autocomplete(request):
    print(Book.objects.count())

    if 'term' in request.GET:
        qs = Book.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)
        print(titles)

        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    return render(request,"home.html")

def homepage(request):
    return render(request, "homepage.html")
