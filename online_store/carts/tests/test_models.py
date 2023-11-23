import pytest
from django.contrib.auth.models import User
from shop.models import Book, Genre
from carts.models import Cart, CartItem

@pytest.fixture
def create_user():
    def _create_user(username='testuser', password='testpass12345'):
        return User.objects.create_user(username=username, password=password)

    return _create_user

@pytest.fixture
def create_book():
    def _create_book(title='Test Book',description='Test Description', author='Test Author', price=20.0, discounted_price=15.0, is_published=True,slug='test-book'):
        return Book.objects.create(title=title, description=description, author=author, price=price, discounted_price=discounted_price, is_published=is_published, slug=slug)

    return _create_book

@pytest.fixture
def create_cart(create_user):
    def _create_cart(user=None):
        user = user or create_user()
        return Cart.objects.create(user=user)
    
    return _create_cart

@pytest.mark.django_db(transaction=True)
def test_create_cart(create_cart):
    cart = create_cart()
    assert Cart.objects.count() == 1
    assert cart.user is not None

@pytest.mark.django_db(transaction=True)
def test_add_book_to_cart(create_cart, create_book):
    cart = create_cart()
    book = create_book()

    cart_item = CartItem.objects.create(cart=cart, book=book, quantity=1)

    assert CartItem.objects.count() == 1
    assert cart_item.cart == cart
    assert cart_item.book == book
    assert cart_item.quantity == 1

@pytest.mark.django_db(transaction=True)
def test_add_duplicate_book_to_cart(create_cart, create_book):
    cart = create_cart()
    book = create_book()

    # Добавление книги в корзину
    cart_item = CartItem.objects.create(cart=cart, book=book, quantity=1)

    # Обновление объекта cart_item после добавления еще одного экземпляра книги в корзину
    cart_item.quantity = 2
    cart_item.save()

    # Проверка, что у нас по-прежнему один объект CartItem с общим количеством 2
    assert CartItem.objects.count() == 1
    assert cart_item.cart == cart
    assert cart_item.book == book
    assert cart_item.quantity == 2