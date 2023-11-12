from django import forms
from profiles.models import UserProfile
from shop.models import Book

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("first_name", 'last_name', 'address', 'phone_number', 'profile_picture')