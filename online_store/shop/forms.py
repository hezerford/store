from django import forms
from .models import *

class BookSearchForm(forms.Form):
    query = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Book name'}))