from django.test import TestCase
from unittest.mock import patch, MagicMock
from .views import search_books

# Create your tests here.

class SearchBooksTests(TestCase):
    @patch('search.views.get_book_bst')
    def test_search_books_with_valid_query(self, mock_get_book_bst):
        # Mock the BST search results
        mock_title_bst = MagicMock()
        mock_author_bst = MagicMock()
        mock_genre_bst = MagicMock()

        mock_title_bst.search.return_value = ['Book1', 'Book2']
        mock_author_bst.search.return_value = ['Book3']
        mock_genre_bst.search.return_value = ['Book4', 'Book2']

        mock_get_book_bst.return_value = (mock_title_bst, mock_author_bst, mock_genre_bst)

        # Call the function
        results = search_books(query="test", limit=5)

        # Verify the results
        self.assertEqual(len(results), 4)
        self.assertIn('Book1', results)
        self.assertIn('Book2', results)
        self.assertIn('Book3', results)
        self.assertIn('Book4', results)

    @patch('search.views.get_book_bst')
    def test_search_books_with_empty_query(self, mock_get_book_bst):
        # Call the function with an empty query
        results = search_books(query="", limit=5)

        # Verify the results are empty
        self.assertEqual(results, [])

    @patch('search.views.get_book_bst')
    def test_search_books_with_limit(self, mock_get_book_bst):
        # Mock the BST search results
        mock_title_bst = MagicMock()
        mock_author_bst = MagicMock()
        mock_genre_bst = MagicMock()

        mock_title_bst.search.return_value = ['Book1', 'Book2', 'Book3']
        mock_author_bst.search.return_value = ['Book4']
        mock_genre_bst.search.return_value = ['Book5', 'Book6']

        mock_get_book_bst.return_value = (mock_title_bst, mock_author_bst, mock_genre_bst)

        # Call the function with a limit
        results = search_books(query="test", limit=3)

        # Verify the results are limited
        self.assertEqual(len(results), 3)