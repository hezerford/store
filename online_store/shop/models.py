from django.db import models
from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название жанра')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Book(models.Model):
    title = models.CharField(max_length=75, verbose_name='Название книги')
    description = models.TextField(max_length=750, verbose_name='Описание')
    author = models.CharField(max_length=50, verbose_name='Автор')
    price = models.IntegerField(verbose_name='Цена')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано да/нет')
    genre = models.ManyToManyField(Genre)
    discounted_price = models.IntegerField(verbose_name='Цена со скидкой', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Book_detail", kwargs={"book_slug": self.slug})

    class Meta:
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
        ordering = ['time_create', 'title']

class Quote(models.Model):
    quote = models.CharField(max_length=255, verbose_name='Цитата')
    author_quote = models.CharField(max_length=50, verbose_name='Автор цитаты')
    
    def __str__(self):
        return self.author_quote

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'Цитаты'

class Email(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email