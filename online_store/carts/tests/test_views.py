import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from django.test import RequestFactory
from carts.views import CartView, AddToCartView, RemoveFromCartView
from shop.models import Book
from carts.models import Cart, CartItem

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

@pytest.mark.django_db(transaction=True)
def test_cart_view(create_user, create_cart):
    # Создаем GET-запрос
    request = RequestFactory().get(reverse('cart'))

    # Принудительно аутентифицируем запрос
    request.user = create_user

    # Передаем GET-запрос в представление
    response = CartView.as_view()(request)

    # Проверяем статус-код
    assert response.status_code == 200

@pytest.mark.django_db(transaction=True)
def test_add_to_cart_view(create_user, create_book, create_cart_item):
    # Создаем POST-запрос
    request = RequestFactory().post(reverse('add-to-cart', kwargs={'book_slug': create_book.slug}))

    # Передаем во view нашего аутентифицированного созданного пользователя
    request.user = create_user

    # Передаем POST-запрос в представление
    response = AddToCartView.as_view()(request, book_slug=create_book.slug)

    # Проверяем статус-код
    assert response.status_code == 302

@pytest.mark.django_db(transaction=True)
def test_remove_from_cart_view(create_user, create_book, create_cart_item):
    # Создаем POST-запрос
    request = RequestFactory().post(reverse('remove-from-cart', kwargs={'book_slug': create_book.slug}))

    # Передаем во view нашего аутентифицированного созданного пользователя
    request.user = create_user

    # Передаем POST-запрос в представление
    response = RemoveFromCartView.as_view()(request, book_slug=create_book.slug)

    # Проверяем статус-код
    assert response.status_code == 302