from django_filters import rest_framework as filters

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from shop.models import Book

from .filters import *
from .serializers import BookSerializer, BookDetailSerializer

class AllBooksAPI(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  

class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [IsAuthenticated]

class DiscountedBookListView(generics.ListAPIView):
    queryset = Book.objects.filter(discounted_price__isnull=False)
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookSearchAPI(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter
    permission_classes = [IsAuthenticated]
