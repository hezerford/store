import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory

from profiles.models import UserProfile
from profiles.views import ProfileDetailView, ProfileUpdateView
from mixer.backend.django import mixer

from bs4 import BeautifulSoup

@pytest.fixture
def create_user():
    return mixer.blend(User, username="testuser")

@pytest.fixture
def create_user_profile(create_user):
    return mixer.blend(UserProfile, user=create_user, phone_number='+1234567890')

@pytest.fixture
def authenticated_client(create_user):
    client = RequestFactory().get(reverse('profile-detail', kwargs={'username': 'testuser'}))
    client.user = create_user
    return client

@pytest.mark.django_db(transaction=True)
def test_profile_detail_view(authenticated_client, create_user_profile):
    # Используем RequestFactory для создания запроса с параметром username
    request = RequestFactory().get(reverse('profile-detail', kwargs={'username': 'testuser'}))
    request.user = authenticated_client.user

    # Вызываем представление с запросом
    response = ProfileDetailView.as_view()(request, username='testuser')

    assert response.status_code == 200
    assert 'user_profile' in response.context_data
    assert response.context_data['user_profile'] == create_user_profile
    response.render()
    content_str = response.content.decode('utf-8')
    # Используем BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(content_str, 'lxml')

    # Находим все теги <p> с классом "fs-5"
    paragraphs = soup.find_all('p', class_='fs-5')

    # Проверяем каждый параграф
    for paragraph in paragraphs:
        if 'First name:' in paragraph.get_text():
            assert paragraph.get_text() == 'First name: ' + create_user_profile.first_name
        elif 'Last name:' in paragraph.get_text():
            assert paragraph.get_text() == 'Last name: ' + create_user_profile.last_name
        elif 'Address:' in paragraph.get_text():
            assert paragraph.get_text() == 'Address: ' + create_user_profile.address
        elif 'Phone:' in paragraph.get_text():
            assert paragraph.get_text().replace('  ', ' ').strip() == 'Phone: ' + str(create_user_profile.phone_number).strip()

@pytest.fixture
def updated_data():
    return {
        'first_name': 'Updated First Name',
        'last_name': 'Updated Last Name',
        'address': 'Updated Address',
        'phone_number': '+9876543210',
    }

@pytest.mark.django_db(transaction=True)
def test_profile_update_view(authenticated_client, create_user_profile, updated_data):
    # Используем RequestFactory для создания запроса
    request = RequestFactory().post(reverse('profile-update', kwargs={'username': 'testuser'}))

    request.user = authenticated_client.user

    # Вызываем представление с запросом
    response = ProfileUpdateView.as_view()(request)

    # Обновляем данные профиля
    create_user_profile.first_name = updated_data['first_name']
    create_user_profile.last_name = updated_data['last_name']
    create_user_profile.address = updated_data['address']
    create_user_profile.phone_number = updated_data['phone_number']
    create_user_profile.save()

    # Проверяем успешность обновления профиля
    assert response.status_code == 302

    # Проверяем, что профиль обновлен
    create_user_profile.refresh_from_db()
    assert create_user_profile.first_name == 'Updated First Name'
    assert create_user_profile.last_name == 'Updated Last Name'
    assert create_user_profile.address == 'Updated Address'
    assert str(create_user_profile.phone_number) == '+9876543210'

    # Проверяем URL-адрес перенаправления
    assert response.url == reverse('profile-detail', kwargs={'username': create_user_profile.user.username})