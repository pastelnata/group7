from django.test import TestCase
from books.models import Book
from ...search.bst_manager import get_book_bst, search_books

class SearchComponentTests(TestCase):
    def setUp(self):
        # Create mock book data in the database
        Book.objects.create(title="The Great Gatsby", author="F. Scott Fitzgerald", category_name="Fiction")
        Book.objects.create(title="To Kill a Mockingbird", author="Harper Lee", category_name="Fiction")
        Book.objects.create(title="1984", author="George Orwell", category_name="Dystopian")
        Book.objects.create(title="A", author="Herman Melville", category_name="Adventure")

    def test_get_book_bst(self):
        # Test that BSTs are built correctly
        title_bst, author_bst, genre_bst = get_book_bst()
        self.assertIsNotNone(title_bst.root)
        self.assertIsNotNone(author_bst.root)
        self.assertIsNotNone(genre_bst.root)

    def test_search_books_by_title(self):
        # Test searching by title
        results = search_books(query="1984", limit=10)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "1984")

    def test_search_books_by_author(self):
        # Test searching by author
        results = search_books(query="Harper Lee", limit=10)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Harper Lee")

    def test_search_books_by_genre(self):
        # Test searching by genre
        results = search_books(query="Fiction", limit=10)
        self.assertEqual(len(results), 2)
        self.assertTrue(any(book.title == "The Great Gatsby" for book in results))
        self.assertTrue(any(book.title == "To Kill a Mockingbird" for book in results))

    def test_search_books_combined_results(self):
        # Test combined results from all BSTs
        results = search_books(query="a", limit=10)
        self.assertEqual(len(results), 4)

    def test_search_books_empty_query(self):
        # Test with an empty query
        results = search_books(query="", limit=10)
        self.assertEqual(len(results), 0)

    def test_search_books_no_results(self):
        # Test with no matching results
        results = search_books(query="Nonexistent Book", limit=10)
        self.assertEqual(len(results), 0)

    def test_search_books_case_insensitive(self):
        # Test case-insensitive search
        results = search_books(query="the great gatsby", limit=10)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "The Great Gatsby")