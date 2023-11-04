from django.urls import path
from .views import *

urlpatterns = [
    path('', BookHome.as_view(), name='home'),
    path('search/', BookSearchView, name='book-search'),
    
    path('book/<slug:book_slug>/', BookDetailView.as_view(), name='book-detail'),
    path('books/', AllBooks.as_view(), name='all-books'),

    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='view_profile'),
]
