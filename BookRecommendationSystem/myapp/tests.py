from django.test import TestCase, Client
from django.urls import reverse
from .forms import SupportForm
from books.models import Book
from django.core.mail import outbox

class MyAppViewTests(TestCase):
    def test_autocomplete_view(self):
        # Test the autocomplete view
        Book.objects.create(title="Test Book 1")
        Book.objects.create(title="Another Test Book")
        response = self.client.get(reverse('autocomplete') + '?term=Test')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            ['Test Book 1', 'Another Test Book']
        )

class MyAppFormTests(TestCase):
    def test_contact_form_valid(self):
        # Test a valid contact form
        form_data = {
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'content': 'Test message content.'
        }
        form = SupportForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_invalid(self):
        # Test an invalid contact form (missing email)
        form_data = {
            'subject': 'Test Subject',
            'content': 'Test message content.'
        }
        form = SupportForm(data=form_data)
        self.assertFalse(form.is_valid())