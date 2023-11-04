from django.urls import path
from .views import *

urlpatterns = [
    path('api/all-books/', AllBooksAPI.as_view(), name='all-books-api'),
    path('api/discounted-books/', DiscountedBookListView.as_view(), name='discounted-books-api'),
    path('api/book-search/', BookSearchAPI.as_view(), name='book-search-api'),
    path('api/books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail-api'),
]