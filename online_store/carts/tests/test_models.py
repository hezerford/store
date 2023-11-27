import pytest
from django.contrib.auth.models import User
from shop.models import Book, Genre
from mixer.backend.django import mixer
from carts.models import Cart, CartItem

@pytest.fixture
def create_user():
    return User.objects.create_user(username='testuser', password='testpass12345')

@pytest.fixture
def create_book():
    return mixer.blend(Book, photo=None)

@pytest.fixture
def create_cart(create_user):
    return Cart.objects.create(user=create_user)

@pytest.mark.django_db(transaction=True)
def test_create_cart(create_cart):
    assert Cart.objects.count() == 1
    assert create_cart.user is not None

@pytest.mark.django_db(transaction=True)
def test_add_book_to_cart(create_cart, create_book):
    cart_item = CartItem.objects.create(cart=create_cart, book=create_book, quantity=1)

    assert CartItem.objects.count() == 1
    assert cart_item.cart == create_cart
    assert cart_item.book == create_book
    assert cart_item.quantity == 1

@pytest.mark.django_db(transaction=True)
def test_add_duplicate_book_to_cart(create_cart, create_book):
    # Добавление книги в корзину
    cart_item = CartItem.objects.create(cart=create_cart, book=create_book, quantity=1)

    # Обновление объекта cart_item после добавления еще одного экземпляра книги в корзину
    cart_item.quantity = 2
    cart_item.save()

    # Проверка, что у нас по-прежнему один объект CartItem с общим количеством 2
    assert CartItem.objects.count() == 1
    assert cart_item.cart == create_cart
    assert cart_item.book == create_book
    assert cart_item.quantity == 2