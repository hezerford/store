import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from django.test import RequestFactory
from carts.views import CartView, AddToCartView, RemoveFromCartView
from shop.models import Book
from carts.models import Cart, CartItem
from rest_framework.test import force_authenticate

@pytest.fixture
def create_user():
    return mixer.blend(User)

@pytest.fixture
def create_book():
    return mixer.blend(Book, photo=None)

@pytest.fixture
def create_cart(create_user):
    return mixer.blend(Cart, user=create_user)

@pytest.fixture
def create_cart_item(create_cart, create_book):
    return mixer.blend(CartItem, cart=create_cart, book=create_book)

@pytest.fixture
def authenticated_client(create_user):
    client = RequestFactory().post(reverse('add-to-cart', kwargs={'book_slug': 'your-book-slug'}))
    client.user = create_user
    return client

@pytest.mark.django_db
def test_cart_view(create_cart):
    # Создаем объект RequestFactory
    factory = RequestFactory()

    # Создаем GET-запрос
    request = factory.get(reverse('cart'))

    # Создаем пользователя
    user = User.objects.create_user(username='testuser', password='testpass12345')

    # Принудительно аутентифицируем запрос
    request.user = user

    # Передаем GET-запрос в представление
    response = CartView.as_view()(request)

    # Проверяем статус-код
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_to_cart_view(authenticated_client, create_book, create_cart):
    url = reverse('add-to-cart', kwargs={'book_slug': create_book.slug})
    response = AddToCartView.as_view()(authenticated_client, book_slug=create_book.slug)
    assert response.status_code == 302  # Redirect status code

@pytest.mark.django_db
def test_remove_from_cart_view(authenticated_client, create_book, create_cart_item):
    url = reverse('remove-from-cart', kwargs={'book_slug': create_book.slug})
    response = RemoveFromCartView.as_view()(authenticated_client, book_slug=create_book.slug)
    assert response.status_code == 302  # Redirect status code