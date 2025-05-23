from django.shortcuts import render

from books.models import Book
from .search.bst_manager import search_books
from .sorting.get_top10 import get_top10_books
from .sorting.merge_sort import merge_sort
from recommendation.graph.bfs import bfs  # Import your bfs function


def convert_to_dict(book):
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'category_name': book.category_name,
        'stars': str(book.stars),
        'price': str(book.price),
        'imgURL': book.imgURL,
        'productURL': book.productURL,
        'isBestSeller': book.isBestSeller,
        'isEditorsPick': book.isEditorsPick,
        'isGoodReadsChoice': book.isGoodReadsChoice
    }

def sort_book_list(books, query, sort_by):
    if not books:
        return []
    books_list = [convert_to_dict(book) for book in books]
    sorted_list = merge_sort(books_list, query, sort_by)
    return [Book.objects.get(id=book['id']) for book in sorted_list]

def search_results(request):
    query = request.GET.get('query', '')
    sort_by = request.GET.get('sort', 'relevance')
    results = search_books(query)

    suggestions = []
    author_suggestion = None

    if results:
        results = sort_book_list(results, query, sort_by)
        start_book = results[0]
        start_id = start_book.id

        try:
            # BFS-based related books (excluding the searched one)
            related_books = bfs(start_id, return_books=True)
            suggestions = [book for book in related_books if book.id != start_id][:3]

             # Sort recommendations
            suggestions = sort_book_list(suggestions, query, sort_by)

            # Author-based suggestion (excluding the searched one and any in `suggestions`)
            author_books = Book.objects.filter(author=start_book.author).exclude(id=start_id)
            for book in author_books:
                if book not in suggestions:
                    author_suggestion = book
                    break
            
            if author_suggestion:
                author_suggestions = [author_suggestion]
                sorted_author = sort_book_list(author_suggestions, query, sort_by)
                author_suggestion = sorted_author[0] if sorted_author else None

        except Exception as e:
            print(f"BFS error: {e}")

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


    