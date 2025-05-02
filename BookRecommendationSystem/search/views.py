from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from books.models import Book
from .sorting.get_top10 import get_top10_books
from .search.bst_manager import search_books 
from search.graph import build_book_graph, bfs_recommendations

def search_results(request):
    query = request.GET.get('query', '')
    results = search_books(query)  # BST search
    
    recommended = []
    if results:
        first_result = results[0]
        # Limit to top 100 books for graph building to prevent memory overload
        graph = build_book_graph(limit=100)  # You can adjust this limit as necessary
        recommended = bfs_recommendations(first_result.id, graph, limit=10)
    
    return render(request, 'search_results.html', {
        'results': results,
        'query': query,
        'recommended': recommended,
    })

def top10_results(request):
    top10s = get_top10_books()
    return render(request, 'top10.html', {'top10s': top10s})

def recommended_books(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    graph = build_book_graph()
    recommended = bfs_recommendations(book.id, graph, limit=10)

    print("Recommended Books:", recommended)

    data = [{
        'id': b.id,
        'title': b.title,
        'author': b.author,
        'category': b.category_name
    } for b in recommended]

    return JsonResponse(data, safe=False)

