from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'address', 'phone_number']
class BookSearchForm(forms.Form):
    query = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Book name'}))