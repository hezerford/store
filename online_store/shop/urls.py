from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', BookHome.as_view(), name='home'),
    path('book/<slug>/', BookDetailView.as_view(), name='book-detail'),
    path('books/', AllBooks.as_view(), name='all-books'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout, name='logout'),
]
