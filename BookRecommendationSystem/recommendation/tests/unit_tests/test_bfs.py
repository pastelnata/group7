from django.test import TestCase
from unittest.mock import patch, MagicMock
from recommendation.graph.bfs import bfs

class BFSTests(TestCase):
    @patch('recommendation.graph.bfs.build_graph_adj_list')
    def test_bfs_with_valid_start_node(self, mock_build_graph_adj_list):
        # Mock graph data
        mock_adj = {1: [2, 3], 2: [1, 4], 3: [1], 4: [2]}
        mock_book_lookup = {
            1: MagicMock(id=1, title="Book1"),
            2: MagicMock(id=2, title="Book2"),
            3: MagicMock(id=3, title="Book3"),
            4: MagicMock(id=4, title="Book4"),
        }
        mock_build_graph_adj_list.return_value = (mock_adj, mock_book_lookup)

        # Call BFS
        result = bfs(start_node_id=1)

        # Verify traversal order
        self.assertEqual(result, [1, 2, 3, 4])

    @patch('recommendation.graph.bfs.build_graph_adj_list')
    def test_bfs_with_invalid_start_node(self, mock_build_graph_adj_list):
        # Mock graph data
        mock_adj = {1: [2, 3], 2: [1, 4], 3: [1], 4: [2]}
        mock_book_lookup = {
            1: MagicMock(id=1, title="Book1"),
            2: MagicMock(id=2, title="Book2"),
            3: MagicMock(id=3, title="Book3"),
            4: MagicMock(id=4, title="Book4"),
        }
        mock_build_graph_adj_list.return_value = (mock_adj, mock_book_lookup)

        # Call BFS with invalid start node
        with self.assertRaises(ValueError):
            bfs(start_node_id=99)

    @patch('recommendation.graph.bfs.build_graph_adj_list')
    def test_bfs_with_return_books(self, mock_build_graph_adj_list):
        # Mock graph data
        mock_adj = {1: [2, 3], 2: [1, 4], 3: [1], 4: [2]}
        mock_book_lookup = {
            1: MagicMock(id=1, title="Book1"),
            2: MagicMock(id=2, title="Book2"),
            3: MagicMock(id=3, title="Book3"),
            4: MagicMock(id=4, title="Book4"),
        }
        mock_build_graph_adj_list.return_value = (mock_adj, mock_book_lookup)

        # Call BFS with return_books=True
        result = bfs(start_node_id=1, return_books=True)

        # Verify returned books
        self.assertEqual([book.title for book in result], ["Book1", "Book2", "Book3", "Book4"])
