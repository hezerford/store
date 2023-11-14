from django.test import TestCase
from shop.forms import BookSearchForm

class BookSearchFormTest(TestCase):

    def test_form_valid(self):
        data = {'query': 'Harry Potter'}
        form = BookSearchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_empty_query(self):
        data = {'query': ''}
        form = BookSearchForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('query', form.errors.keys())
        self.assertIn('This field is required.', form.errors['query'])
    
    def test_form_invalid_long_query(self):
        data = {'query': 'a' * 101}
        form = BookSearchForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('query', form.errors.keys())
        self.assertIn('Ensure this value has at most 100 characters (it has 101).', form.errors['query'][0])