from books.models import Book
from .heap_sort import HeapSort

def get_books_by_categories(category):
    return Book.objects.filter(category_name=category).only('stars', 'title', 'author', 'price', 'imgURL', 'productURL')

def get_top10_books():
    categories = ['Romance', 'Mystery, Thriller & Suspense', 'History', 'Health, Fitness & Dieting', 'Science Fiction & Fantasy', 'Education & Teaching']
    top_books = {}

    for category in categories:
        books = get_books_by_categories(category)

        top10s = sort_by_stars(books)

        books_dict = get_book_info(top10s)

        top_books[category] = [
            {
                'title': books_dict[book_id].title,
                'stars': books_dict[book_id].stars,
                'author': books_dict[book_id].author,
                'price': books_dict[book_id].price,
                'imgURL': books_dict[book_id].imgURL,
                'productURL': books_dict[book_id].productURL,
            }
            for stars, book_id in top10s
        ]

    return top_books

def sort_by_stars(books):
    books_with_stars = [(book.stars, book.id) for book in books]
    top_books_for_category = HeapSort.topK(books_with_stars, 10)
    return top_books_for_category

def get_book_info(books):
    book_ids = [book_id for _, book_id in books]
    books_dict = {book.id: book for book in Book.objects.filter(id__in=book_ids)}
    return books_dict