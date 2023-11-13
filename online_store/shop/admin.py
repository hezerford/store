from django.contrib import admin
from .models import Book, Genre, Quote

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'price', 'discounted_price', 'photo', 'is_published')
    filter_vertical = ('genre',)
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title", )}

admin.site.register(Book, BookAdmin)

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Genre, GenreAdmin)

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote', 'author_quote')
    search_fields = ('quote', 'author_quote')

admin.site.register(Quote, QuoteAdmin)