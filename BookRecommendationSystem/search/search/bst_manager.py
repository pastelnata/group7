from books.models import Book
from .bst import BookBST
import time

def get_book_bst():
    """Get or create the BSTs from cache"""

    books = Book.objects.only('title', 'author', 'category_name')

    start_time = time.time()

    author_bst = build_bst('author', books)
    title_bst = build_bst('title', books)
    genre_bst = build_bst('category_name', books)

    end_time = time.time()

    print('BSTs built in:', end_time - start_time, 'seconds')

    return title_bst, author_bst, genre_bst

def build_bst(key, books):
    bst = BookBST(key=key)
    bst.build_from_queryset(books)
    return bst

def search_books(query, limit=25):
    """Search for books using BST"""
    if not query:
        return []
    
    print('getting book bsts...')
    title_bst, author_bst, genre_bst = get_book_bst()
    print('Bsts built.')

    print('searching...')
    title_results = title_bst.search(query, limit // 3)
    author_results = author_bst.search(query, limit // 3)
    genre_results = genre_bst.search(query, limit // 3)
    print('search done.')

    combined_results = []
    seen_books = set()

    for book in title_results + author_results + genre_results:
        if book not in seen_books:
            combined_results.append(book)
            seen_books.add(book)

    # Limit the combined results
    return combined_results[:limit]