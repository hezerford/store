from django import forms
from .models import *

from profiles.models import UserProfile

class BookSearchForm(forms.Form):
    query = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Book name'}))

class FavoriteBooksForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['favorite_books']