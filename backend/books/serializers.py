
  # СЕРИАЛИЗАТОРЫ — books/serializers.py


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Author, Book, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category          
        fields = ['id', 'name', 'slug', 'description']


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'full_name', 'bio', 'birth_date', 'photo']

    def get_full_name(self, obj):

        return f'{obj.first_name} {obj.last_name}'


class ReviewSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'username', 'rating', 'text', 'created_at']

        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):

        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookListSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    authors = AuthorSerializer(many=True, read_only=True)

    average_rating = serializers.ReadOnlyField()   
    reviews_count = serializers.ReadOnlyField()     

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'category', 'authors',
            'published_year', 'cover',
            'average_rating', 'reviews_count'
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    authors = AuthorSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    reviews_count = serializers.ReadOnlyField()

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,  
        required=False
    )
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='authors',
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'isbn',
            'published_year', 'pages', 'cover',
            'category', 'category_id',
            'authors', 'author_ids',
            'reviews', 'average_rating', 'reviews_count',
            'created_at', 'updated_at'
        ]
