from django.test import TestCase
from ...models import Book

class BookModelTests(TestCase):
    def setUp(self):
        # Create a sample book for testing
        self.book = Book.objects.create(
            asin="B001234567",
            title="Sample Book",
            author="John Doe",
            soldBy="Sample Seller",
            productURL="http://example.com/book",
            imgURL="http://example.com/image.jpg",
            stars=4,
            reviews=100,
            price=20,
            isKindleUnlimited=True,
            category_id=1,
            isBestSeller=True,
            isEditorsPick=False,
            isGoodReadsChoice=True,
            published_date="2023-01-01",
            category_name="Fiction"
        )

    def test_book_str_representation(self):
        # Test the __str__ method of the Book model
        self.assertEqual(str(self.book), "Sample Book")

    def test_book_field_constraints(self):
        # Test unique constraint on asin
        with self.assertRaises(Exception):
            Book.objects.create(
                asin="B001234567",  # Duplicate ASIN
                title="Another Book"
            )

        # Test null constraint on title
        with self.assertRaises(Exception):
            Book.objects.create(
                asin="B009876543",
                title=None  # Title cannot be null
            )

    def test_book_creation(self):
        # Test that a book can be created successfully
        book = Book.objects.create(
            asin="B009876543",
            title="Another Sample Book",
            author="Jane Doe",
            soldBy="Another Seller",
            productURL="http://example.com/another-book",
            imgURL="http://example.com/another-image.jpg",
            stars=5,
            reviews=50,
            price=15,
            isKindleUnlimited=False,
            category_id=2,
            isBestSeller=False,
            isEditorsPick=True,
            isGoodReadsChoice=False,
            published_date="2023-02-01",
            category_name="Non-Fiction"
        )
        self.assertEqual(book.title, "Another Sample Book")
        self.assertEqual(book.stars, 5)