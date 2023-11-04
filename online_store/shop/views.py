from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin

from carts.models import Cart, CartItem

from .forms import *
from .models import *
from .utils import *

from random import choice

class BookHome(ListView):
    model = Book
    template_name = 'shop/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Home'
        context['form'] = BookSearchForm(self.request.GET)

        query = self.request.GET.get('query')

        if query:
            books = Book.objects.filter(title__icontains=query)
            context['books'] = books

        books_with_related_data = Book.objects.only('title', 'description', 'price', 'photo', 'discounted_price').prefetch_related(
            Prefetch('genre', queryset=Genre.objects.only('name')),
        )

        discounted_books = [book for book in books_with_related_data if book.discounted_price is not None]

        context['discounted_books'] = discounted_books

        context['pop_books'] = books_with_related_data
        context['feature_books'] = books_with_related_data[:4]

        random_book = choice(books_with_related_data)
        context['random_book'] = random_book

        quotes = Quote.objects.all()
        random_quote = choice(quotes)
        context['random_quote'] = random_quote
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'shop/book.html'
    context_object_name = 'book'
    slug_field = 'slug'
    slug_url_kwarg = 'book_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Book'

        book = self.object  # Объект книги

        if book.discounted_price:
            old_price = book.price
            discounted_price = book.discounted_price
        else:
            old_price = None
            discounted_price = book.price

        context['old_price'] = old_price
        context['discounted_price'] = discounted_price

        if self.request.user.is_authenticated:
            # Корзина текущего аутентифицированного пользователя
            cart, created = Cart.objects.get_or_create(user=self.request.user)

            # Проверить, есть ли книга в корзине
            created = CartItem.objects.filter(cart=cart, book=book).exists()
        else:
            # Для анонимных пользователей, устанавливаем cart в None и created в False
            cart = None
            created = False

        context['cart'] = cart
        context['created'] = created

        return context

def BookSearchView(request):
    form = BookSearchForm(request.GET)
    books = []

    if form.is_valid():
        query = form.cleaned_data['query']
        books = Book.objects.filter(title__icontains=query)
    
    context = {'form': form, 'books': books}
    return render(request, 'shop/search_results.html', context)

class AllBooks(ListView):
    model = Book
    template_name = 'shop/all_books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'All Books'
        context['books'] = Book.objects.all()
        return context