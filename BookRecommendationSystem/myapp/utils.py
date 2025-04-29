# This file should be saved as myapp/utils.py

from .merge_sort import merge_sort
from .models import Book

def get_sorted_books(sort_key='stars', order='desc', filters=None):
    """
    Get books from the database and sort them using merge sort.
    
    Parameters:
    sort_key (str): Field to sort by ('stars', 'reviews', 'price', 'published_date')
    order (str): Sort order - 'asc' for ascending, 'desc' for descending
    filters (dict): Optional filter criteria for the query
    
    Returns:
    list: Sorted list of books
    """
    # Start with all books
    queryset = Book.objects.all()
    
    # Apply any filters
    if filters:
        queryset = queryset.filter(**filters)
    
    # Convert queryset to list for sorting
    books_list = list(queryset)
    
    # Apply merge sort
    sorted_books = merge_sort(books_list, sort_key, order)
    
    return sorted_books