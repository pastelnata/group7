import time
from django.shortcuts import render

from books.models import Book
from .search.bst_manager import search_books
from .sorting.get_top10 import get_top10_books
from .sorting.merge_sort import merge_sort
from recommendation.graph.bfs import bfs

def sort_book_list(books, sort_by):
    if not books or sort_by == 'relevance':
        return list(books)
    return merge_sort(books, sort_by)

def search_results(request):
    start_time = time.time()
    query = request.GET.get('query', '')
    sort_by = request.GET.get('sort', 'relevance')
    results = search_books(query)
    end_time_search = time.time()
    print(f"search duration: {end_time_search - start_time:.4f}s")

    suggestions = []
    author_suggestion = None

    if results:
        start_time_sort = time.time()
        results = sort_book_list(results, sort_by)
        end_time_sort = time.time()
        print(f"Sort duration: {end_time_sort - start_time_sort:.4f}s")

        start_book = results[0]
        start_id = start_book.id

        try:
            start_time_bfs = time.time()
            # BFS-based related books (excluding the searched one)
            related_books = bfs(start_id, return_books=True)
            suggestions = [book for book in related_books if book.id != start_id][:3]
            end_time_bfs = time.time()
            print(f"BFS duration: {end_time_bfs - start_time_bfs:.4f}s")

            # Sort recommendations
            start_time_suggestion_sort = time.time()
            suggestions = sort_book_list(suggestions, sort_by)
            end_time_suggestion_sort = time.time()
            print(f"Suggestion sort duration: {end_time_suggestion_sort - start_time_suggestion_sort:.4f}s")

            # Author-based suggestion (excluding the searched one and any in `suggestions`)
            start_time_author = time.time()
            author_books = Book.objects.filter(author=start_book.author).exclude(id=start_id)
            for book in author_books:
                if book not in suggestions:
                    author_suggestion = book
                    break

            if author_suggestion:
                author_suggestions = [author_suggestion]
                sorted_author = sort_book_list(author_suggestions, sort_by)
                author_suggestion = sorted_author[0] if sorted_author else None
            end_time_author = time.time()
            print(f"Author suggestion duration: {end_time_author - start_time_author:.4f}s")

        except Exception as e:
            print(f"BFS error: {e}")

    end_time = time.time()
    print(f"total duration: {end_time - start_time:.4f}s")

    return render(request, 'search_results.html', {
        'results': results,
        'suggestions': suggestions,
        'author_suggestion': author_suggestion,
        'query': query,
        'sort_by': sort_by
    })

def top10_results(request):
    top10s = get_top10_books()
    return render(request, 'top10.html', {'top10s': top10s})


    