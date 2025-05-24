import json
from django.test import RequestFactory, TestCase
from unittest.mock import patch, MagicMock

from ...views import get_recommendations
from ...recommendation import get_graph_recommendations, calculate_recommendation_scores

class RecommendationTests(TestCase):
	@patch('books.recommendation.serialize_book', autospec=True)
	def test_get_graph_recommendations_basic(self, mock_serialize):
		book1 = MagicMock(id=1)
		book2 = MagicMock(id=2)
		book3 = MagicMock(id=3)
		book_lookup = {1: book1, 2: book2, 3: book3}
		recommendation_scores = {1: 5.0, 2: 10.0, 3: 7.0}
		filtered_book_ids = {2}
		mock_serialize.side_effect = lambda b: {'id': b.id}

		result = get_graph_recommendations(recommendation_scores, book_lookup, filtered_book_ids, limit=2)

		# Should sort by score descending, skip id=2, limit to 2
		self.assertEqual(result, [{'id': 3}, {'id': 1}])
		mock_serialize.assert_any_call(book3)
		mock_serialize.assert_any_call(book1)
		self.assertEqual(mock_serialize.call_count, 2)

	def test_calculate_recommendation_scores_basic(self):
		filtered_book_ids = [1]
		adj = {1: [2, 3]}
		book2 = MagicMock(stars=4, reviews=5)
		book3 = MagicMock(stars=3, reviews=2)
		book_lookup = {2: book2, 3: book3}
		
		result = calculate_recommendation_scores(filtered_book_ids, adj, book_lookup)
		
		self.assertEqual(result[2], 20)  # 4*5
		self.assertEqual(result[3], 6)   # 3*2