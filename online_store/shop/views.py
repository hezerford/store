from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .forms import *
from .models import *
from .utils import *

class BookHome(ListView):
    model = Book
    template_name = 'shop/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Home'
        context['pop_books'] = Book.objects.all()[:8]
        context['feature_books'] = Book.objects.all()[:4]
        context['quotes'] = Quote.objects.all()
        return context
    

class BookDetailView(DetailView):
    model = Book
    template_name = 'shop/book.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Book'
        return context
    
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
        return context

    def get_success_url(self):
        return reverse_lazy('home')

def logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')