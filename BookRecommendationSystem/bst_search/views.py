from django.core.cache import cache
from myapp.models import Book  # Using the existing Book model
from .bst import BookBST

def get_book_bst():
    """Get or create the BST from cache"""
    bst = cache.get('book_bst')
    if bst is None:
        bst = BookBST()
        bst.build_from_queryset(Book.objects.all())
        cache.set('book_bst', bst, timeout=3600)  # Cache for 1 hour
    return bst

def search_books(query, limit=25):
    """Search for books using BST"""
    if not query:
        return []
    
    bst = get_book_bst()
    return bst.search(query, limit) 