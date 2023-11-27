import os
import pytest
from django.test import Client, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from shop.views import Home, BookDetailView, AddToFavoritesView, RemoveFromFavoritesView, BookSearchView, AllBooks
from shop.models import Book, Genre, Quote
from profiles.models import UserProfile
from django.contrib.auth.models import User

@pytest.fixture
def create_user():
    return mixer.blend(User)

@pytest.fixture
def create_user_profile(create_user):
    return mixer.blend(UserProfile, user=create_user, phone_number='+1234567890')

@pytest.fixture
def create_book():
    return mixer.blend(Book)

@pytest.fixture
def create_quote():
    return mixer.blend(Quote)

@pytest.mark.django_db(transaction=True)
def test_book_home_view(create_book, create_quote):
    request = RequestFactory().get(reverse('home'))
    response = Home.as_view()(request)

    image_path = create_book.photo.path
    if os.path.exists(image_path):
        os.remove(image_path)

    assert response.status_code == 200
    assert 'title' in response.context_data
    assert 'form' in response.context_data
    assert 'book_list' in response.context_data
    
@pytest.mark.django_db(transaction=True)
def test_book_detail_view(create_user, create_user_profile, create_book):
    request = RequestFactory().get(reverse('book-detail', kwargs={'book_slug': create_book.slug}))
    request.user = create_user
    response = BookDetailView.as_view()(request, book_slug=create_book.slug)

    image_path = create_book.photo.path
    if os.path.exists(image_path):
        os.remove(image_path)

    assert response.status_code == 200
    assert 'title' in response.context_data
    assert 'book' in response.context_data
    assert 'old_price' in response.context_data
    assert 'discounted_price' in response.context_data
    assert 'book_in_favorites' in response.context_data
    assert 'created' in response.context_data
    assert 'in_cart' in response.context_data
    assert 'cart' in response.context_data

    image_path = create_book.photo.path
    if os.path.exists(image_path):
        os.remove(image_path)

@pytest.mark.django_db(transaction=True)
def test_add_to_favorites_view(create_user, create_user_profile, create_book):
    # Отправляем POST-запрос на добавление в избранное
    request = RequestFactory().post(reverse('add-to-favorites', kwargs={'book_slug': create_book.slug}))
    request.user = create_user
    response = AddToFavoritesView.as_view()(request, book_slug=create_book.slug)

    image_path = create_book.photo.path
    if os.path.exists(image_path):
        os.remove(image_path)

    # Проверяем, что статус код равен 302 (редирект)
    assert response.status_code == 302

    # Проверяем, что книга добавлена в избранное у пользователя
    create_user.refresh_from_db()
    assert create_book in create_user_profile.favorite_books.all()

@pytest.mark.django_db(transaction=True)
def test_remove_from_favorites_view(create_user, create_user_profile, create_book):

    # Добавляем книгу в избранное у пользователя
    create_user.userprofile.favorite_books.add(create_book)

    # Отправляем POST-запрос на удаление из избранного
    request = RequestFactory().post(reverse('remove-from-favorites', kwargs={'book_slug': create_book.slug}))
    request.user = create_user
    response = RemoveFromFavoritesView.as_view()(request, book_slug=create_book.slug)

    image_path = create_book.photo.path
    if os.path.exists(image_path):
        os.remove(image_path)

    # Проверяем, что статус код равен 302 (редирект)
    assert response.status_code == 302

    # Проверяем, что книга удалена из избранного у пользователя
    create_user.refresh_from_db()
    assert create_book not in create_user_profile.favorite_books.all()

@pytest.mark.django_db(transaction=True)
def test_book_search_view():
    # Создаем книги
    books = [
        mixer.blend(Book, title="Python for Beginners"),
        mixer.blend(Book, title="Django Web Development")
    ]

    # Удаляем фото книг из БД
    for book in books:
        os.remove(book.photo.path)

    # Отправляем GET-запрос на страницу поиска
    request = RequestFactory().get(reverse('book-search'), {'query': 'Python'})
    response = BookSearchView.as_view()(request)

    # Проверяем, что статус код равен 200
    assert response.status_code == 200

    # Проверяем, что книга с именем "Python for Beginners" присутствует в контексте
    assert 'Python for Beginners' in response.content.decode('utf-8')

    # Проверяем, что книга с именем "Django Web Development" отсутствует в контексте
    assert 'Django Web Development' not in response.content.decode('utf-8')
