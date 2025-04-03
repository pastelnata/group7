from django.shortcuts import render
from .bst_manager import search_books

def search_results(request):
    query = request.GET.get('query', '')
    results = search_books(query)
    return render(request, 'search_results.html', {'results': results, 'query': query})