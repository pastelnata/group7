from django.test import TestCase
from unittest.mock import patch, MagicMock
from search.sorting.get_top10 import get_top10_books, get_books_by_categories, sort_by_stars, get_book_info
from books.models import Book

class TestGetTop10Books(TestCase):
    @patch('search.sorting.get_top10.get_books_by_categories')
    @patch('search.sorting.get_top10.sort_by_stars')
    @patch('search.sorting.get_top10.get_book_info')
    def test_get_top10_books(self, mock_get_book_info, mock_sort_by_stars, mock_get_books_by_categories):
        # Mock data
        mock_books = [
            MagicMock(id=1, title="Book 1", stars=4.5, author="Author 1", price=10.99, imgURL="url1", productURL="product1"),
            MagicMock(id=2, title="Book 2", stars=4.0, author="Author 2", price=12.99, imgURL="url2", productURL="product2"),
        ]
        mock_get_books_by_categories.return_value = mock_books
        mock_sort_by_stars.return_value = [(4.5, 1), (4.0, 2)]
        mock_get_book_info.return_value = {1: mock_books[0], 2: mock_books[1]}

        # Call the function
        result = get_top10_books()

        # Assertions
        self.assertIn('Romance', result)
        self.assertEqual(len(result['Romance']), 2)
        self.assertEqual(result['Romance'][0]['title'], "Book 1")
        self.assertEqual(result['Romance'][1]['title'], "Book 2")

    @patch('search.sorting.get_top10.Book.objects.filter')
    def test_get_books_by_categories(self, mock_filter):
        # Mock QuerySet
        mock_queryset = MagicMock()
        mock_queryset.only.return_value = [
            MagicMock(stars=4.5, title="Book 1", author="Author 1", price=10.99, imgURL="url1", productURL="product1"),
            MagicMock(stars=4.0, title="Book 2", author="Author 2", price=12.99, imgURL="url2", productURL="product2"),
        ]
        mock_filter.return_value = mock_queryset

        # Call the function
        result = get_books_by_categories("Romance")

        # Assertions
        mock_filter.assert_called_once_with(category_name="Romance")
        mock_queryset.only.assert_called_once_with('stars', 'title', 'author', 'price', 'imgURL', 'productURL')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, "Book 1")
        self.assertEqual(result[1].title, "Book 2")

    @patch('search.sorting.get_top10.HeapSort.topK')
    def test_sort_by_stars(self, mock_topK):
        # Mock data
        mock_books = [
            MagicMock(stars=4.5, id=1),
            MagicMock(stars=4.0, id=2),
        ]
        mock_topK.return_value = [(4.5, 1), (4.0, 2)]

        # Call the function
        result = sort_by_stars(mock_books)

        # Assertions
        mock_topK.assert_called_once_with([(4.5, 1), (4.0, 2)], 10)
        self.assertEqual(result, [(4.5, 1), (4.0, 2)])

    @patch('search.sorting.get_top10.Book.objects.filter')
    def test_get_book_info(self, mock_filter):
        # Mock data
        mock_books = [
            MagicMock(id=1, title="Book 1"),
            MagicMock(id=2, title="Book 2"),
        ]
        mock_filter.return_value = mock_books

        # Call the function
        result = get_book_info([(4.5, 1), (4.0, 2)])

        # Assertions
        mock_filter.assert_called_once_with(id__in=[1, 2])
        self.assertEqual(result[1].title, "Book 1")
        self.assertEqual(result[2].title, "Book 2")