from django.shortcuts import render
from .search.bst_manager import search_books
from .sorting.get_top10 import get_top10_books

def search_results(request):
    query = request.GET.get('query', '')
    results = search_books(query)
    return render(request, 'search_results.html', {'results': results, 'query': query})

def top10_results(request):
    top10s = get_top10_books()
    return render(request, 'top10.html', {'top10s': top10s})