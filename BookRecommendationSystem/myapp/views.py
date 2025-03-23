import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Book
# Create your views here.

def libraryview(request):
    event_list=Book.objects.all()
    return render(request,"libraryview.html", {'event_list': event_list })

def autocomplete(request):
    if 'term' in request.GET:
        qs = Book.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)

        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
    return render(request,"home.html")