from django.contrib import admin
from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('items',)

admin.site.register(Cart, CartAdmin)