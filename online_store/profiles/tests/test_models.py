import pytest
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from mixer.backend.django import mixer
from profiles.models import UserProfile

@pytest.fixture
def create_user_profile():
    return mixer.blend(UserProfile, phone_number='+1234567890')

@pytest.mark.django_db(transaction=True)
def test_user_profile_creation(create_user_profile):
    # Получите профиль пользователя
    profile = UserProfile.objects.get(id=create_user_profile.id)

    assert profile.user.username is not None
    assert profile.user.first_name is not None
    assert profile.user.last_name is not None
    assert profile.address is not None
    assert profile.phone_number is not None
    assert profile.profile_picture is not None