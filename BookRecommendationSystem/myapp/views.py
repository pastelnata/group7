import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

# Create your views here.
#from .models import Library


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