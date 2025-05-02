from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from books.models import Book
from .sorting.get_top10 import get_top10_books
from .search.bst_manager import search_books 
from search.graph import build_book_graph, bfs_recommendations

def search_results(request):
    query = request.GET.get('query', '')
    book_id = request.GET.get('book_id')  # Get book_id if available from the request

    # Get search results
    results = search_books(query)
    
    recommended = []
    selected_book = None
    
    # If a book is selected, fetch its details and recommendations
    if book_id:
        selected_book = get_object_or_404(Book, id=book_id)
        graph = build_book_graph()
        recommended = bfs_recommendations(selected_book.id, graph, limit=10)

    # Otherwise, use the first result for recommendations
    elif results:
        first_result = results[0]
        graph = build_book_graph()
        recommended = bfs_recommendations(first_result.id, graph, limit=10)

    return render(request, 'search_results.html', {
        'results': results,
        'query': query,
        'recommended': recommended,
        'selected_book': selected_book,
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

