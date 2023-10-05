from django.contrib import admin
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'price', 'discounted_price', 'photo', 'is_published')
    filter_vertical = ('genre',)
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title", )}

admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Quote)