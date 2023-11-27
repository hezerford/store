import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from mixer.backend.django import mixer
from shop.models import Book
from django.contrib.auth.models import User

@pytest.fixture
def create_book():
    def _create_book(**kwargs):
        return mixer.blend(Book, photo=None, **kwargs)
    
    return _create_book

@pytest.fixture
def authenticated_client():
    user = User.objects.create_user(username='testuser', password='testpass12345')
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.mark.django_db(transaction=True)
def test_all_books_api(authenticated_client, create_book):
    # Создаем хотя бы одну книгу для тестирования
    create_book()

    url = reverse('all-books-api')
    response = authenticated_client.get(url)  
    assert response.status_code == status.HTTP_200_OK

    # Проверить, что response.data - это список
    assert isinstance(response.data, list)

    # Проверить, что список не пустой
    assert len(response.data) > 0

    # Проверить ключи в первом словаре списка
    first_book = response.data[0]
    assert 'title' in first_book
    assert 'description' in first_book
    assert 'author' in first_book
    assert 'genre' in first_book
    assert 'price' in first_book


@pytest.mark.django_db(transaction=True)
def test_book_detail_api(authenticated_client, create_book):
    book = create_book()
    url = reverse('book-detail-api', kwargs={'pk': book.pk})
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert 'title' in response.data
    assert 'description' in response.data
    assert 'author' in response.data
    assert 'genre' in response.data
    assert 'price' in response.data

@pytest.mark.django_db(transaction=True)
def test_discounted_book_list_api(authenticated_client, create_book):
    # Создаем несколько книг, некоторые из которых имеют скидочные цены
    create_book(title='Book1',description='Book1 Description', author='Book1 Author', price=20.0, discounted_price=15.0, is_published=True, slug='book1')
    create_book(title='Book2',description='Book2 Description', author='Book2 Author', price=14.0, discounted_price=12.0, is_published=True, slug='book2')
    create_book(title='Book3',description='Book3 Description', author='Book3 Author', price=10.0, discounted_price=None, is_published=True, slug='book3')

    url = reverse('discounted-books-api')
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert isinstance(response.data, list)
    assert len(response.data) == 2  # ожидаем две книги с скидочными ценами


@pytest.mark.django_db(transaction=True)
def test_book_search_api(authenticated_client, create_book):
    # Создаем несколько книг для тестирования поиска
    create_book(title='Python Book', description='Learn Python programming', author='Python Author', price=20.0, discounted_price=15.0, slug='python-book')
    create_book(title='Django Book', description='Building web applications with Django', author='Django Author', price=14.0, discounted_price=12.0, is_published=True, slug='django-book')
    create_book(title='Java Book', description='Introduction to Java programming', author='Java Author', price=10.0, is_published=True, slug='java-book')

    url = reverse('book-search-api')
    response = authenticated_client.get(url, {'title': 'Python'})
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что в ответе есть данные и они соответствуют ожидаемой структуре
    assert isinstance(response.data, list)
    assert len(response.data) == 1  # Ожидаем только одну книгу с соответствующим заголовком