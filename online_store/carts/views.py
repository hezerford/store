from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *

class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'carts/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = None  # Инициализируем корзину как None

        cart, created = Cart.objects.get_or_create(user=user)

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

        # если в корзине уже есть книга данного экземпляра, то она не создается, а прибавляется в кол-ве
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