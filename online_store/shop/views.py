from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Prefetch


from django_filters import rest_framework as filters

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .filters import BookFilter
from .forms import *
from .models import *
from .utils import *
from .serializers import BookSerializer, BookDetailSerializer

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
    
    # def purchase_book(self):
    #     book = self.get_object()
    #     book.sales_count += 1
    #     book.save()

    #     # Логика обработки платежей и заказов

    #     return redirect('home')

def BookSearchView(request):
    form = BookSearchForm(request.GET)
    books = []

    if form.is_valid():
        query = form.cleaned_data['query']
        books = Book.objects.filter(title__icontains=query)
    
    context = {'form': form, 'books': books}
    return render(request, 'shop/search_results.html', context)

@method_decorator(login_required, name='dispatch')
class CartView(TemplateView):
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = None  # Инициализируем cart как None

        if user.is_authenticated:  # Проверяем, аутентифицирован ли пользователь
            cart, created = Cart.objects.get_or_create(user=user)
        else:  # Если пользователь анонимный
            session_cart_id = self.request.session.get('cart_id')
            if session_cart_id:
                cart, created = Cart.objects.get_or_create(id=session_cart_id)
            else:
                cart = Cart.objects.create()
                self.request.session['cart_id'] = cart.id

        cart_items = CartItem.objects.filter(cart=cart)
        total_price = 0

        for cart_item in cart_items:
            book = cart_item.book
            if book.discounted_price:
                total_price += book.discounted_price * cart_item.quantity
            else:
                total_price += book.price * cart_item.quantity

        context["cart"] = cart
        context["cart_items"] = cart_items
        context["total_price"] = total_price
        context["created"] = created
        return context
    
class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, slug=kwargs['book_slug'])

        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user) # Если объект существует,  он будет присвоен переменной cart, и created будет равно False, потому что объект был найден, но не создан. Если объекта не существовало, то он будет создан, присвоен переменной cart, и created будет равно True, потому что объект был создан.
        else:
            cart, created = Cart.objects.get_or_create(user=None)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book) # Также как и выше

        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return redirect('cart')

class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, slug=kwargs['book_slug'])

        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, book=book)
        cart_item.quantity -= 1
        cart_item.save()

        return redirect('home')
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