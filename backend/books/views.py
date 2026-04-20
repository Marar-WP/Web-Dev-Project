from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from .models import Category, Author, Book, Review
from .serializers import (
    CategorySerializer, AuthorSerializer,
    BookListSerializer, BookDetailSerializer, ReviewSerializer
)
from .permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'bio']
    ordering_fields = ['last_name', 'first_name']


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('category').prefetch_related('authors', 'reviews__user')

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'authors__first_name', 'authors__last_name', 'description']
    ordering_fields = ['title', 'published_year', 'created_at']

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return BookDetailSerializer
        return BookListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(authors__id=author_id)

        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(published_year=year)

        return queryset

    @action(
        detail=True,
        methods=['get', 'post'],
        url_path='reviews',
        permission_classes=[permissions.AllowAny],
    )
    def reviews(self, request, pk=None):
        book = self.get_object()

        if request.method == 'GET':
            reviews = book.reviews.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)

        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Login is required to leave a review.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if Review.objects.filter(book=book, user=request.user).exists():
            return Response(
                {'detail': 'You have already left a review for this book.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReviewSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='top-rated')
    def top_rated(self, request):
        books = self.get_queryset()
        rated_books = [(book, book.average_rating) for book in books if book.average_rating]
        rated_books.sort(key=lambda x: x[1], reverse=True)
        top_books = [book for book, _ in rated_books[:10]]

        serializer = BookListSerializer(top_books, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.select_related('user', 'book').all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ======================
# FBV
# ======================

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def top_rated_books_fbv(request):
    books = Book.objects.select_related('category').prefetch_related('authors', 'reviews__user')
    rated_books = [(book, book.average_rating) for book in books if book.average_rating]
    rated_books.sort(key=lambda x: x[1], reverse=True)
    top_books = [book for book, _ in rated_books[:10]]

    serializer = BookListSerializer(top_books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def book_reviews_fbv(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'GET':
        reviews = book.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if not request.user.is_authenticated:
        return Response(
            {'detail': 'Login is required to leave a review.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if Review.objects.filter(book=book, user=request.user).exists():
        return Response(
            {'detail': 'You have already left a review for this book.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = ReviewSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save(book=book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================
# CBV
# ======================

class CategoryListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        authors = Author.objects.all().order_by('last_name', 'first_name')
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)