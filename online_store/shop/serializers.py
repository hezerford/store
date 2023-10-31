from rest_framework import serializers
from .models import Book, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', )

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = ('title', 'description', 'author', 'price', 'genre', 'discounted_price')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['genre'] = [genre.name for genre in instance.genre.all()]
        return data

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'description', 'author', 'genre', 'photo', 'price', 'discounted_price', 'is_published')