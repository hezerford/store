from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

from .forms import *

from shop.utils import DataMixin
from accounts.forms import LoginUserForm, RegisterUserForm

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/register.html'
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
    template_name = 'accounts/login.html'

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