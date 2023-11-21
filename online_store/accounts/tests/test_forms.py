from django.test import Client
import pytest
from django.contrib.auth.models import User
from accounts.forms import RegisterUserForm, LoginUserForm

@pytest.mark.django_db
def test_register_user_form_valid_data():
    form_data = {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
    }
    form = RegisterUserForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_regiser_user_form_invalid_data():
    form_data = {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'wrongpassword',
    }
    form = RegisterUserForm(data=form_data)
    assert not form.is_valid()
    assert 'password2' in form.errors

@pytest.mark.django_db
def test_succcesful_login():
    # Создаем тестового пользователя
    username = 'testuser'
    password = 'testpass12345'
    user = User.objects.create_user(username=username, password=password)

    client = Client()

    # Пытаемся залогиниться с корректными учетными данными
    logged_in = client.login(username=username, password=password)
    assert logged_in is True

    # Проверка что мы залогинены
    response = client.get('http://127.0.0.1:8000/cart/')
    assert response.status_code == 200
    assert '_auth_user_id' in client.session

@pytest.mark.django_db
def test_login_user_form_invalid_data():
    form_data = {
        'username': 'nonexistentuser',
        'password': 'wrongpassword',
    }
    form = LoginUserForm(data=form_data)
    assert not form.is_valid()
    assert '__all__' in form.errors

