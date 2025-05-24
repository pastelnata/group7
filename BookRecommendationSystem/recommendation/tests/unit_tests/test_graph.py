from django.test import TestCase
from unittest.mock import patch, MagicMock
from recommendation.graph.graph import build_graph_adj_list, get_cached_graph

class GraphAdjacencyTests(TestCase):
    @patch('recommendation.graph.graph.Book')
    @patch('recommendation.graph.graph.group_by_category')
    @patch('recommendation.graph.graph.cache')
    def test_build_graph_adj_list_basic(self, mock_cache, mock_group_by_category, mock_book_cls):
        # Setup: 2 books in category A, 1 in B
        mock_book1 = MagicMock(id=1, category_id=10, category_name="A")
        mock_book2 = MagicMock(id=2, category_id=10, category_name="A")
        mock_book3 = MagicMock(id=3, category_id=20, category_name="B")
        mock_book_cls.objects.only.return_value = [mock_book1, mock_book2, mock_book3]
        mock_cache.get.return_value = None
        mock_group_by_category.return_value = {
            "A": [1, 2],
            "B": [3]
        }

        adj, book_lookup = build_graph_adj_list()
        self.assertEqual(set(adj[1]), {2})
        self.assertEqual(set(adj[2]), {1})
        self.assertEqual(adj[3], [])
        self.assertEqual(book_lookup, {1: mock_book1, 2: mock_book2, 3: mock_book3})

    @patch('recommendation.graph.graph.cache')
    def test_get_cached_graph_returns_from_cache(self, mock_cache):
        mock_cache.get.return_value = ({1: [2]}, {1: "book1"})
        adj, book_lookup = get_cached_graph()
        self.assertEqual(adj, {1: [2]})
        self.assertEqual(book_lookup, {1: "book1"})