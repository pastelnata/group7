from django.test import TestCase
from search.sorting.merge_sort import merge_sort, calculate_relevance_score

class MergeSortTests(TestCase):
    def setUp(self):
        self.books = [
            {
                'title': 'Python 101',
                'author': 'John Doe',
                'category_name': 'Programming',
                'stars': 4.5,
                'price': 25.0,
                'isBestSeller': True,
                'isEditorsPick': False,
                'isGoodReadsChoice': False,
                'search_query': 'python'
            },
            {
                'title': 'Django for Beginners',
                'author': 'Jane Smith',
                'category_name': 'Web Development',
                'stars': 4.8,
                'price': 30.0,
                'isBestSeller': False,
                'isEditorsPick': True,
                'isGoodReadsChoice': True,
                'search_query': 'django'
            },
            {
                'title': 'Learning JavaScript',
                'author': 'Alice',
                'category_name': 'Programming',
                'stars': 4.0,
                'price': 20.0,
                'isBestSeller': False,
                'isEditorsPick': False,
                'isGoodReadsChoice': False,
                'search_query': 'javascript'
            }
        ]

    def test_merge_sort_by_rating(self):
        sorted_books = merge_sort(self.books, sort_by='rating')
        ratings = [book['stars'] for book in sorted_books]
        self.assertEqual(ratings, [4.8, 4.5, 4.0])

    def test_merge_sort_by_price_high(self):
        sorted_books = merge_sort(self.books, sort_by='price_high')
        prices = [book['price'] for book in sorted_books]
        self.assertEqual(prices, [30.0, 25.0, 20.0])

    def test_merge_sort_by_price_low(self):
        sorted_books = merge_sort(self.books, sort_by='price_low')
        prices = [book['price'] for book in sorted_books]
        self.assertEqual(prices, [20.0, 25.0, 30.0])

    def test_merge_sort_by_relevance(self):
        # Add a book with a title exactly matching the search query for high relevance
        books = self.books + [{
            'title': 'django',
            'author': 'Someone',
            'category_name': 'Web',
            'stars': 3.0,
            'price': 15.0,
            'isBestSeller': False,
            'isEditorsPick': False,
            'isGoodReadsChoice': False,
            'search_query': 'django'
        }]
        sorted_books = merge_sort(books, sort_by='relevance')
        scores = [calculate_relevance_score(book, book.get('search_query', '')) for book in sorted_books]
        self.assertEqual(scores, sorted(scores, reverse=True))