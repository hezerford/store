from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Prefetch

from .forms import *
from .models import *
from .utils import *

from random import choice

class BookHome(ListView):
    model = Book
    template_name = 'shop/main.html'
    
    # def get_most_sold_book(self):
    #     most_sold_book = Book.objects.order_by('-sales_count').first()
    #     return most_sold_book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Home'

        books_with_related_data = Book.objects.only('title', 'description', 'price', 'photo', 'discounted_price').prefetch_related(
            Prefetch('genre', queryset=Genre.objects.only('name')),
        )

        context['pop_books'] = books_with_related_data
        context['feature_books'] = books_with_related_data[:4]

        random_book = choice(books_with_related_data)
        context['random_book'] = random_book

        quotes = Quote.objects.all()
        random_quote = choice(quotes)
        context['random_quote'] = random_quote
        # context['most_sold_book'] = self.get_most_sold_book()
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

        book = self.object # Объект книги

        if book.discounted_price:
            old_price = book.price
            discounted_price = book.discounted_price
        else:
            old_price = None
            discounted_price = book.price

        context['old_price'] = old_price
        context['discounted_price'] = discounted_price

        return context
    
    # def purchase_book(self):
    #     book = self.get_object()
    #     book.sales_count += 1
    #     book.save()

    #     # Логика обработки платежей и заказов

    #     return redirect('home')
    
class AllBooks(ListView):
    model = Book
    template_name = 'shop/all_books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'All Books'
        context['books'] = Book.objects.all()
        return context
    

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Authorization'
        context['username'] = self.request.user.username if self.request.user.is_authenticated else None
        return context

    def get_success_url(self):
        return reverse_lazy('home')

class LogoutUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('home')