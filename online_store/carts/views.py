from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View

from .models import *

@method_decorator(login_required, name='dispatch')
class CartView(TemplateView):
    template_name = 'carts/cart.html'

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
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect('home')