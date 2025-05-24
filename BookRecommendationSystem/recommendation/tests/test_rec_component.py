import json
from django.test import TestCase, Client
from django.urls import reverse
from books.models import Book

class RecommendationComponentTests(TestCase):
    def setUp(self):
        # Create books with different tags, categories, prices, and ratings
        self.book1 = Book.objects.create(
            title="Book 1", author="Author 1", category_name="Romance", stars=4.5, price=0,
            isBestSeller=True, isEditorsPick=False, isGoodReadsChoice=False, isKindleUnlimited=False
        )
        self.book2 = Book.objects.create(
            title="Book 2", author="Author 1", category_name="Mystery", stars=4.7, price=0,
            isBestSeller=True, isEditorsPick=False, isGoodReadsChoice=False, isKindleUnlimited=False
        )
        self.book3 = Book.objects.create(
            title="Book 3", author="Author 3", category_name="History", stars=4.8, price=0,
            isBestSeller=True, isEditorsPick=False, isGoodReadsChoice=False, isKindleUnlimited=False
        )
        self.book4 = Book.objects.create(
            title="Book 4", author="Author 4", category_name="Romance", stars=4.6, price=0,
            isBestSeller=True, isEditorsPick=False, isGoodReadsChoice=False, isKindleUnlimited=False
        )
        self.book5 = Book.objects.create(
            title="Book 5", author="Author 5", category_name="Fantasy", stars=4.9, price=0,
            isBestSeller=True, isEditorsPick=False, isGoodReadsChoice=False, isKindleUnlimited=False
        )
        self.client = Client()

    def test_recommendation(self):
        # User selects 1 tag, 4 categories, 1 price range, 1 minimum rating
        payload = {
            "tags": ["bestseller"],
            "genres": ["Romance", "Mystery", "History", "Science Fiction"],
            "price": "free",
            "rating": 4.5
        }
        response = self.client.post(
            reverse('get_recommendations'),
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('recommendations', data)
        # All returned books should match the filters
        for book in data['recommendations']:
            self.assertIn(book['category'], payload['genres'])
            self.assertGreaterEqual(float(book['rating']), payload['rating'])
            self.assertEqual(book['is_bestseller'], True)
            self.assertEqual(float(book['price']), 0)

    def test_search_recommendation(self):
        # Simulate a search for 'Romance'
        response = self.client.get(
            reverse('search_results') + '?query=Romance'
        )
        self.assertEqual(response.status_code, 200)
        # Check context data
        self.assertIn('results', response.context)
        self.assertIn('suggestions', response.context)
        self.assertIn('author_suggestion', response.context)

        # 1. The first search result should be a Romance book
        results = response.context['results']

        # 2. Suggestions should be books in the same category (excluding the first result)
        suggestions = response.context['suggestions']
        for book in suggestions:
            self.assertEqual(book.category_name, "Romance")
            self.assertNotEqual(book.id, results[0].id)

        # 3. Author suggestion should be a book by the same author, not the searched book
        author_suggestion = response.context['author_suggestion']
        if author_suggestion:
            self.assertEqual(author_suggestion.author, results[0].author)