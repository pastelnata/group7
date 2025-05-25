from django.test import TestCase
from unittest.mock import patch, MagicMock
from ...filter_books import filter_books_by_criteria, filter_by_genres, filter_by_price, filter_by_rating, filter_by_tags,	serialize_book

class FilterBooksTests(TestCase):

	def test_filter_by_genres_with_genres(self):
		mock_qs = MagicMock()
		genres = ['Fiction', 'Sci-Fi']
		result = filter_by_genres(mock_qs, genres)
		mock_qs.filter.assert_called_once_with(category_name__in=genres)
		self.assertEqual(result, mock_qs.filter())

	def test_filter_by_genres_without_genres(self):
		mock_qs = MagicMock()
		result = filter_by_genres(mock_qs, [])
		mock_qs.filter.assert_not_called()
		self.assertEqual(result, mock_qs)

	def test_filter_by_price_free(self):
		mock_qs = MagicMock()
		result = filter_by_price(mock_qs, 'free')
		mock_qs.filter.assert_called_once_with(price=0)
		self.assertEqual(result, mock_qs.filter())

	def test_filter_by_price_under5(self):
		mock_qs = MagicMock()
		result = filter_by_price(mock_qs, 'under5')
		mock_qs.filter.assert_called_once_with(price__lt=500)
		self.assertEqual(result, mock_qs.filter())

	def test_filter_by_price_any(self):
		mock_qs = MagicMock()
		result = filter_by_price(mock_qs, 'any')
		mock_qs.filter.assert_not_called()
		self.assertEqual(result, mock_qs)

	def test_filter_by_rating_valid(self):
		mock_qs = MagicMock()
		result = filter_by_rating(mock_qs, '4')
		mock_qs.filter.assert_called_once_with(stars__gte=4)
		self.assertEqual(result, mock_qs.filter())

	def test_filter_by_rating_invalid(self):
		mock_qs = MagicMock()
		result = filter_by_rating(mock_qs, 'bad')
		mock_qs.filter.assert_not_called()
		self.assertEqual(result, mock_qs)

	def test_filter_by_rating_any(self):
		mock_qs = MagicMock()
		result = filter_by_rating(mock_qs, 'any')
		mock_qs.filter.assert_not_called()
		self.assertEqual(result, mock_qs)

	def test_filter_by_tags_bestseller(self):
		mock_qs = MagicMock()
		result = filter_by_tags(mock_qs, ['bestseller'])  # Pass as a list
		mock_qs.filter.assert_called_once_with(isBestSeller=True)
		self.assertEqual(result, mock_qs.filter())

	def test_filter_by_tags_none(self):
		mock_qs = MagicMock()
		result = filter_by_tags(mock_qs, [])
		mock_qs.filter.assert_not_called()
		self.assertEqual(result, mock_qs)