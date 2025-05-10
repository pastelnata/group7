from django.test import TestCase
from books.models import Book
from search.search.bst_manager import get_book_bst, search_books
from search.sorting.get_top10 import get_top10_books
from search.search.graph import build_graph_adj_list
from search.search.bfs import bfs

class BooksComponentTests(TestCase):
    def setUp(self):
        # Create mock book data in the database with specified categories
        self.book1 = Book.objects.create(
            asin="B001234567",
            title="Pride and Prejudice",
            author="Jane Austen",
            category_name="Romance",
            stars=4.6,
            reviews=180
        )

        self.book2 = Book.objects.create(
            asin="B002345678",
            title="Gone Girl",
            author="Gillian Flynn",
            category_name="Mystery, Thriller & Suspense",
            stars=4.8,
            reviews=250
        )
        
        self.book3 = Book.objects.create(
            asin="B003456789",
            title="Sapiens: A Brief History of Humankind",
            author="Yuval Noah Harari",
            category_name="History",
            stars=4.7,
            reviews=300
        )

        self.book4 = Book.objects.create(
            asin="B004567890",
            title="The Body Keeps the Score",
            author="Bessel van der Kolk",
            category_name="Health, Fitness & Dieting",
            stars=4.9,
            reviews=400
        )

        self.book5 = Book.objects.create(
            asin="B005678901",
            title="Dune",
            author="Frank Herbert",
            category_name="Science Fiction & Fantasy",
            stars=4.8,
            reviews=500
        )

        self.book6 = Book.objects.create(
            asin="B006789012",
            title="The Hobbit",
            author="J.R.R. Tolkien",
            category_name="Science Fiction & Fantasy",
            stars=4.9,
            reviews=600
        )

        self.book7 = Book.objects.create(
            asin="B007890123",
            title="Educated",
            author="Tara Westover",
            category_name="Education & Teaching",
            stars=4.7,
            reviews=350
        )

        self.book8 = Book.objects.create(
            asin="B008901234",
            title="Becoming",
            author="Michelle Obama",
            category_name="History",
            stars=4.8,
            reviews=450
        )

        self.book9 = Book.objects.create(
            asin="B009012345",
            title="Atomic Habits",
            author="James Clear",
            category_name="Health, Fitness & Dieting",
            stars=4.9,
            reviews=550
        )

        self.book10 = Book.objects.create(
            asin="B010123456",
            title="The Silent Patient",
            author="Alex Michaelides",
            category_name="Mystery, Thriller & Suspense",
            stars=4.6,
            reviews=300
        )

    def test_top10(self):
        sorted_books = get_top10_books()

        expected_categories = [
            "Romance",
            "Mystery, Thriller & Suspense",
            "History",
            "Health, Fitness & Dieting",
            "Science Fiction & Fantasy",
            "Education & Teaching"
        ]
        self.assertEqual(set(sorted_books.keys()), set(expected_categories))

        # Validate that each category contains up to 10 books
        for category, books in sorted_books.items():
            self.assertLessEqual(len(books), 10)

        # Validate the order of books within a category (sorted by stars)
        sci_fi_books = sorted_books["Science Fiction & Fantasy"]
        self.assertEqual(sci_fi_books[0]['title'], "The Hobbit")  # Highest stars and reviews
        self.assertEqual(sci_fi_books[-1]['title'], "Dune")  # Lower stars and reviews

    def test_books_to_recommendation(self):
        # Test integration with the recommendation component using BFS and adjacency list

        # Build the adjacency list and book lookup
        adj_list, book_lookup = build_graph_adj_list()

        # Validate adjacency list structure
        self.assertEqual(len(adj_list), 10)
        self.assertIn(self.book2.id, adj_list[self.book10.id])
        self.assertIn(self.book5.id, adj_list[self.book6.id])

        # Perform BFS starting from "Gone Girl"
        bfs_result = bfs(self.book2.id, return_books=True)

        # Validate BFS traversal
        self.assertGreaterEqual(len(bfs_result), 1)  # At least one book should be connected
        self.assertIn(self.book10.id, [book.id for book in bfs_result])  # Check that "The Silent Patient" is recommended