from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.user.username