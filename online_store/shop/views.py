from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, FormView
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

        # Поиск книг по частичному совпадению с заголовком
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
            # Создаем форму для управления избранными книгами
            user_profile = self.request.user.userprofile

            # Создается экземпляр формы FavoriteBooksForm с предварительно заполненными данными (initial)
            # т.е. когда пользователь переходит на страницу с книгой, автоматические берется id книги и вставляется в форму
            # и далее instance связывает форму с существующим экземпляром модели user_profile
            form = FavoriteBooksForm(instance=user_profile, initial={'favorite_books': [book.id]})

            context['favorite_books_form'] = form

            # Есть ли книга в избранном у пользователя
            book_in_favorites = book in user_profile.favorite_books.all()

            # Корзина текущего аутентифицированного пользователя
            cart, created = Cart.objects.get_or_create(user=self.request.user)

            # Проверить, есть ли книга в корзине (если один или несколько объектов True, иначе False)
            created = CartItem.objects.filter(cart=cart, book=book).exists()
        else:
            # Для анонимных пользователей, устанавливаем cart в None и created в False
            cart = None
            created = False
            book_in_favorites = False

        context['cart'] = cart
        context['created'] = created
        context['book_in_favorites'] = book_in_favorites

        return context
    
class AddToFavoritesView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, book_slug):
        book = Book.objects.get(slug=book_slug)
        user_profile = request.user.userprofile

        # Проверяем что книга не в избранном
        if book not in user_profile.favorite_books.all():
            user_profile.favorite_books.add(book)
        
        return redirect('book-detail', book_slug=book_slug)

class RemoveFromFavoritesView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, book_slug):
        user_profile = request.user.userprofile
        book = get_object_or_404(Book, slug=book_slug)

        if book in user_profile.favorite_books.all():
            user_profile.favorite_books.remove(book)
        
        return redirect('book-detail', book_slug=book_slug)

class BookSearchView(View):
    template_name = 'shop/search_results.html'

    def get(self, request, *args, **kwargs):
        form = BookSearchForm(request.GET)
        query = request.GET.get('query')
        books = Book.objects.filter(title__icontains=query) if query else []

        context = {'form': form, 'books': books}
        return render(request, self.template_name, context)
class AllBooks(ListView):
    model = Book
    template_name = 'shop/all_books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'All Books'
        context['books'] = Book.objects.all()
        return context