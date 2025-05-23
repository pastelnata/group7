from django.shortcuts import render

from books.models import Book
from .search.bst_manager import search_books
from .sorting.get_top10 import get_top10_books
from recommendation.graph.bfs import bfs  # Import your bfs function

def search_results(request):
    query = request.GET.get('query', '')
    results = search_books(query)

    suggestions = []
    author_suggestion = None

    if results:
        start_book = results[0]
        start_id = start_book.id

        try:
            # BFS-based related books (excluding the searched one)
            related_books = bfs(start_id, return_books=True)
            suggestions = [book for book in related_books if book.id != start_id][:3]

            # Author-based suggestion (excluding the searched one and any in `suggestions`)
            author_books = Book.objects.filter(author=start_book.author).exclude(id=start_id)
            for book in author_books:
                if book not in suggestions:
                    author_suggestion = book
                    break

        except Exception as e:
            print(f"BFS error: {e}")

    return render(request, 'search_results.html', {
        'results': results,
        'suggestions': suggestions,
        'author_suggestion': author_suggestion,
        'query': query
    })


def top10_results(request):
    top10s = get_top10_books()
    return render(request, 'top10.html', {'top10s': top10s})


    