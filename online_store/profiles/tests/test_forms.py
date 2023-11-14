from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from profiles.forms import FavoriteBooksForm, UserProfileForm
from profiles.models import UserProfile
from shop.models import Book

class UserProfileFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.get_or_create(user=self.user)[0]

    def test_valid_user_profile_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Main St',
            'phone_number': '+1234567890',
            'profile_picture': SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        }
        form = UserProfileForm(data=form_data, instance=self.user_profile)
        
        # Проверяем, что форма не проходит валидацию (не действительна)
        self.assertFalse(form.is_valid())
        
        # Проверяем, что ошибка по полю phone_number присутствует
        self.assertIn('phone_number', form.errors)

    def test_invalid_phone_number_format(self):
        form_data = {
            'phone_number': 'invalid_phone_number',
        }
        form = UserProfileForm(data=form_data, instance=self.user_profile)
        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn('phone_number', form.errors)

    def test_user_profile_form_with_favorite_books(self):
        book1 = Book.objects.create(title='Book 1', price=19.99, slug='book-1')
        book2 = Book.objects.create(title='Book 2', price=29.99, slug='book-2')
        form_data = {
            'favorite_books': [book1.id, book2.id],
        }
        form = UserProfileForm(data=form_data, instance=self.user_profile)
        self.assertNotIn('favorite_books', form.fields)

class FavoriteBooksFormTest(TestCase):

    def setUp(self):
        # Создаем пользователя и UserProfile, если он не существует
        self.user = User.objects.create(username='testuser', password='testpass')
        self.user_profile = UserProfile.objects.get_or_create(user=self.user)[0]

        # Создаем книги
        self.mockingbird_book = Book.objects.create(title='To Kill a Mockingbird', price=19.99, slug='to-kill-a-mockingbird')
        self.gatsby_book = Book.objects.create(title='The Great Gatsby', price=29.99, slug='the-great-gatsby')

        # Создаем форму для каждого теста
        self.form_data = {'favorite_books': [self.gatsby_book.id, self.mockingbird_book.id]}
        self.form = FavoriteBooksForm(data=self.form_data, instance=self.user_profile)

    def test_form_valid(self):
        # Проверяем, что форма считается допустимой с валидными данными
        self.assertTrue(self.form.is_valid())

    def test_form_invalid_empty_books(self):
        # Пытаемся сохранить форму с пустым списком книг
        form_data = {'favorite_books': []}
        form = FavoriteBooksForm(data=form_data, instance=self.user_profile)

        # Проверяем, что форма считается допустимой
        self.assertTrue(form.is_valid())

        # Сохраняем количество книг в favorite_books до сохранения формы
        initial_books_count = self.user_profile.favorite_books.count()

        # Сохраняем форму
        form.save()

        # Перезагружаем UserProfile из базы данных
        updated_user_profile = UserProfile.objects.get(pk=self.user_profile.pk)

        # Проверяем, что количество книг в favorite_books осталось неизменным
        self.assertEqual(updated_user_profile.favorite_books.count(), initial_books_count)

    def test_save_form_updates_user_profile(self):
        # Проверяем, что после сохранения формы, связанный UserProfile обновлен
        form_data = {'favorite_books': [self.gatsby_book.id, self.mockingbird_book.id]}
        form = FavoriteBooksForm(data=form_data, instance=self.user_profile)

        self.assertTrue(form.is_valid())
        form.save()

        # Перезагружаем UserProfile из базы данных
        updated_user_profile = UserProfile.objects.get(pk=self.user_profile.pk)

        # Проверяем, что favorite_books обновлен
        expected_titles = ['The Great Gatsby', 'To Kill a Mockingbird']
        actual_titles = [book.title for book in updated_user_profile.favorite_books.all()]
        self.assertCountEqual(expected_titles, actual_titles)