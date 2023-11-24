import os
import pytest
from django.test import Client, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from shop.views import BookHome
from shop.models import Book, Genre, Quote
from profiles.models import UserProfile
from django.contrib.auth.models import User

@pytest.mark.django_db(transaction=True)
def test_book_home_view():
    genre = mixer.blend(Genre)
    book = mixer.blend(Book, photo=None, genre=[genre])

    mixer.blend(Quote)

    request = RequestFactory().get(reverse('home'))
    response = BookHome.as_view()(request)

    assert response.status_code == 200
    assert 'title' in response.context_data
    assert 'form' in response.context_data
    assert 'book_list' in response.context_data

@pytest.fixture
def create_book():
    return mixer.blend(Book)

@pytest.mark.django_db(transaction=True)
def test_book_detail_view(create_book):
    mixer.blend(Quote)

    client = Client()

    # Логиним пользователя
    user = mixer.blend('auth.User')
    user_profile = mixer.blend(UserProfile, user=user, phone_number='+1234567890')
    client.force_login(user)

    response = client.get(reverse('book-detail', kwargs={'book_slug': create_book.slug}))

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
def test_add_to_favorites_view():
    client = Client()

    # Создаем пользователя
    user = mixer.blend(User)
    user_profile = mixer.blend(UserProfile, user=user, phone_number='+1234567890')
    client.force_login(user)

    # Создаем книгу
    book = mixer.blend(Book)

    # Отправляем POST-запрос на добавление в избранное
    response = client.post(reverse('add-to-favorites', kwargs={'book_slug': book.slug}))

    # Проверяем, что статус код равен 302 (редирект)
    assert response.status_code == 302

    # Проверяем, что книга добавлена в избранное у пользователя
    user.refresh_from_db()
    assert book in user.userprofile.favorite_books.all()

    if os.path.exists(book.photo.path):
        os.remove(book.photo.path)

@pytest.mark.django_db(transaction=True)
def test_remove_from_favorites_view():
    client = Client()

    # Создаем пользователя
    user = mixer.blend(User)
    user_profile = mixer.blend(UserProfile, user=user, phone_number='+1234567890')
    client.force_login(user)

    # Создаем книгу
    book = mixer.blend(Book, photo=None)

    # Добавляем книгу в избранное у пользователя
    user.userprofile.favorite_books.add(book)

    # Отправляем POST-запрос на удаление из избранного
    response = client.post(reverse('remove-from-favorites', kwargs={'book_slug': book.slug}))

    # Проверяем, что статус код равен 302 (редирект)
    assert response.status_code == 302

    # Проверяем, что книга удалена из избранного у пользователя
    user.refresh_from_db()
    assert book not in user.userprofile.favorite_books.all()

@pytest.mark.django_db(transaction=True)
def test_book_search_view():
    client = Client()

    # Создаем книги
    books = [
        mixer.blend(Book, title="Python for Beginners"),
        mixer.blend(Book, title="Django Web Development")
    ]

    # Удаляем книги из БД
    for book in books:
        os.remove(book.photo.path)

    # Отправляем GET-запрос на страницу поиска
    response = client.get(reverse('book-search'), {'query': 'Python'})

    # Проверяем, что статус код равен 200
    assert response.status_code == 200

    # Проверяем, что книга с именем "Python for Beginners" присутствует в контексте
    assert 'Python for Beginners' in str(response.context['books'])

    # Проверяем, что книга с именем "Django Web Development" отсутствует в контексте
    assert 'Django Web Development' not in str(response.context['books'])