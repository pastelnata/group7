from django.shortcuts import render
from .search.bst_manager import search_books
from .sorting.get_top10 import get_top10_books
from .sorting.bfs import bfs  # Import your bfs function

def search_results(request):
    query = request.GET.get('query', '')
    results = search_books(query)

    suggestions = []

    if results:
        # Get the first result's ID to run BFS on
        start_id = results[0].id
        try:
            # Get related books using BFS
            suggestions = bfs(start_id, return_books=True)[0:5]  # Limit to 3
        except Exception as e:
            print(f"BFS error: {e}")

    return render(request, 'search_results.html', {
        'results': results,
        'suggestions': suggestions,
        'query': query
    })

def top10_results(request):
    top10s = get_top10_books()
    return render(request, 'top10.html', {'top10s': top10s})