from books.models import Book
from .heap_sort import HeapSort


books = Book.objects.only('stars')

def get_books_by_categories(category):
    return Book.objects.filter(category_name=category).only('stars', 'title')

def get_top10_books():
    categories = ['Romance', 'Mystery, Thriller & Suspense', 'History', 'Health, Fitness & Dieting', 'Science Fiction & Fantasy', 'Education & Teaching']
    top_books = {}

    for category in categories:
        books = get_books_by_categories(category)
        books_with_stars = [(book.stars, book.title) for book in books] 
        top_books_for_category = HeapSort.topK(books_with_stars, 10) 
        top_books[category] = [title for _, title in top_books_for_category]

    return top_books