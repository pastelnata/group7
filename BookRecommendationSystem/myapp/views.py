import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

# Create your views here.
from .models import Library


def autocomplete(request):
    """     when LIbrary is name of the database
    if 'term' in request.GET:
        qs = Library.objects.filter(title__icontains=request.GET.get('term'))
        titles = list()
        for product in qs:
            titles.append(product.title)

        # titles = [product.title for product in qs]
        return JsonResponse(titles, safe=False)
        """
    return render(request,"home.html")