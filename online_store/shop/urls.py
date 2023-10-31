from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', BookHome.as_view(), name='home'),
    path('search/', BookSearchView, name='book-search'),

    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<slug:book_slug>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/<slug:book_slug>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    
    path('book/<slug:book_slug>/', BookDetailView.as_view(), name='book-detail'),
    path('books/', AllBooks.as_view(), name='all-books'),

    path('api/all-books/', AllBooksAPI.as_view(), name='all-books-api'),
    path('api/discounted-books/', DiscountedBookListView.as_view(), name='discounted-books-api'),
    path('api/book-search/', BookSearchAPI.as_view(), name='book-search-api'),
    path('api/books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail-api'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]
