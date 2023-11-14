from django.test import TestCase
from django.urls import reverse
from shop.models import Genre, Book, Quote, Email

class GenreModelTest(TestCase):

    @classmethod
    def setUp(self):
        # Создаем объект Genre для использования в тестах
        self.genre = Genre.objects.create(name='Тестовый жанр')

    def test_name_label(self):
        # Получаем объект Genre
        genre = Genre.objects.get(id=self.genre.id)
        # Получаем метаданные для поля name и проверяем, что verbose_name соответствует ожиданиям
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название жанра')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=self.genre.id)
        # Получаем метаданные для поля name и проверяем, что max_length соответствует ожиданиям
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_name(self):
        genre = Genre.objects.get(id=self.genre.id)
        # Проверяем, что __str__ метод возвращает правильное значение
        expected_object_name = genre.name
        self.assertEqual(expected_object_name, str(genre))

    def test_verbose_name_plural(self):
        # Проверяем, что verbose_name_plural в мета-классе соответствует ожиданиям
        expected_verbose_name_plural = 'Жанры'
        self.assertEqual(expected_verbose_name_plural, Genre._meta.verbose_name_plural)

class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем объект Genre для использования в тестах
        genre = Genre.objects.create(name='Тестовый жанр')

        # Создаем объект Book для использования в тестах
        cls.book = Book.objects.create(
            title='Тестовая книга',
            description='Описание тестовой книги',
            author='Тестовый автор',
            price=100,
            photo='test.jpg',
            discounted_price=80,
            slug='test-book',
        )
        cls.book.genre.add(genre)

    def test_title_label(self):
        # Проверяем, что verbose_name для поля title соответствует ожиданиям
        field_label = self.book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Название книги')

    def test_description_max_length(self):
        # Проверяем, что max_length для поля description соответствует ожиданиям
        max_length = self.book._meta.get_field('description').max_length
        self.assertEqual(max_length, 1500)

    def test_object_name_is_title(self):
        # Проверяем, что __str__ метод возвращает правильное значение
        expected_object_name = self.book.title
        self.assertEqual(expected_object_name, str(self.book))

    def test_slug_field_unique(self):
        book_duplicate = Book(
            title='Тестовая книга 2',
            description='Описание тестовой книги 2',
            author='Тестовый автор 2',
            price=120,
            photo='test2.jpg',
            discounted_price=100,
            slug='test-book',
        )
        with self.assertRaises(Exception):
            book_duplicate.save()

    def test_get_absolute_url(self):
        # Проверяем, что get_absolute_url возвращает ожидаемый URL
        expected_url = reverse("book-detail", kwargs={"book_slug": self.book.slug})
        self.assertEqual(expected_url, self.book.get_absolute_url())

    def test_verbose_name_plural(self):
        # Проверяем, что verbose_name_plural в мета-классе соответствует ожиданиям
        expected_verbose_name_plural = 'Книги'
        self.assertEqual(expected_verbose_name_plural, Book._meta.verbose_name_plural)

    def test_ordering(self):
        # Проверяем, что книги упорядочены по времени создания и затем по названию
        expected_ordering = ['time_create', 'title']
        self.assertEqual(expected_ordering, Book._meta.ordering)

class QuoteModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем объект Quote для использования в тестах
        Quote.objects.create(quote='Тестовая цитата', author_quote='Тестовый автор')

    def test_quote_label(self):
        quote = Quote.objects.get(id=1)
        # Проверяем, что verbose_name для поля quote соответствует ожиданиям
        field_label = quote._meta.get_field('quote').verbose_name
        self.assertEqual(field_label, 'Цитата')

    def test_author_quote_max_length(self):
        quote = Quote.objects.get(id=1)
        # Проверяем, что max_length для поля author_quote соответствует ожиданиям
        max_length = quote._meta.get_field('author_quote').max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_author_quote(self):
        quote = Quote.objects.get(id=1)
        # Проверяем, что __str__ метод возвращает правильное значение
        expected_object_name = quote.author_quote
        self.assertEqual(expected_object_name, str(quote))

    def test_verbose_name_plural(self):
        # Проверяем, что verbose_name_plural в мета-классе соответствует ожиданиям
        expected_verbose_name_plural = 'Цитаты'
        self.assertEqual(expected_verbose_name_plural, Quote._meta.verbose_name_plural)


class EmailModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаем объект Email для использования в тестах
        Email.objects.create(email='test@example.com')

    def test_email_label(self):
        email = Email.objects.get(id=1)
        # Проверяем, что verbose_name для поля email соответствует ожиданиям
        field_label = email._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'Email')

    def test_email_unique_constraint(self):
        # Пытаемся создать еще один объект Email с тем же адресом, ожидаем ошибку
        with self.assertRaises(Exception):
            Email.objects.create(email='test@example.com')

    def test_object_name_is_email(self):
        email = Email.objects.get(id=1)
        # Проверяем, что __str__ метод возвращает правильное значение
        expected_object_name = email.email
        self.assertEqual(expected_object_name, str(email))