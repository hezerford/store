import os
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

# Вызывается создание профиля при его регистрации на сайте
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Удаляется изображение из файловой системы сайта при сбросе/смене фотографии пользователя
@receiver(pre_delete, sender=UserProfile)
def user_profile_pre_delete(sender, instance, **kwargs):
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)