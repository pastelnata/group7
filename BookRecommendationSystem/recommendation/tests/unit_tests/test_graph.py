from django.test import TestCase
from unittest.mock import patch, MagicMock
from recommendation.graph.bfs import build_graph_adj_list


class GraphTests(TestCase):
    @patch('recommendation.graph.graph.Book.objects.all')
    def test_build_graph_adj_list(self, mock_books_all):
        # Mock Book objects
        mock_book1 = MagicMock(id=1, category_id=101)
        mock_book2 = MagicMock(id=2, category_id=101)
        mock_book3 = MagicMock(id=3, category_id=102)
        mock_books_all.return_value = [mock_book1, mock_book2, mock_book3]

        # Call the function
        adj, book_lookup = build_graph_adj_list()

        adj = dict(adj)

        # Verify adjacency list
        self.assertEqual(adj, {1: [2], 2: [1], 3: []})

        # Verify book lookup
        self.assertEqual(book_lookup, {1: mock_book1, 2: mock_book2, 3: mock_book3})