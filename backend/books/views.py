from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

from .models import Category, Author, Book, Review
from .serializers import (
    CategorySerializer, AuthorSerializer,
    BookListSerializer, BookDetailSerializer, ReviewSerializer
)
from .permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # permission_classes — кто может делать запросы
    # IsAuthenticatedOrReadOnly: читать — все, создавать/изменять — только авторизованные
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # filter_backends — как можно фильтровать и искать
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']   # Поиск по этим полям
    ordering_fields = ['name']                 # Сортировка по этим полям


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet для авторов."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'bio']
    ordering_fields = ['last_name', 'first_name']

@method_decorator(csrf_exempt, name='dispatch')
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('category').prefetch_related('authors', 'reviews__user')
    # select_related  — оптимизация: загружаем category одним JOIN запросом
    # prefetch_related — оптимизация: загружаем авторов и рецензии отдельными оптимальными запросами
    # Без этого при 100 книгах было бы 201+ запрос к БД (N+1 проблема)!

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'authors__first_name', 'authors__last_name', 'description']
    ordering_fields = ['title', 'published_year', 'created_at']

    def get_serializer_class(self):
        """
        Выбираем сериализатор в зависимости от действия.
        list/create    → BookListSerializer   (краткая информация)
        retrieve/update → BookDetailSerializer (полная информация + рецензии)
        """
        if self.action in ['retrieve', 'update', 'partial_update']:
            return BookDetailSerializer
        return BookListSerializer

    def get_queryset(self):
        """
        Позволяем фильтровать книги через URL-параметры.
        Примеры запросов:
          GET /api/books/?category=1
          GET /api/books/?author=2
          GET /api/books/?year=2023
          GET /api/books/?search=гарри
        """
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

    # @action — создаём нестандартные эндпоинты
    # detail=True  → /api/books/{id}/reviews/
    # detail=False → /api/books/popular/
    @action(
    detail=True,
    methods=['get', 'post'],
    url_path='reviews',
    authentication_classes=[CsrfExemptSessionAuthentication],
    permission_classes=[permissions.AllowAny],
)

    def reviews(self, request, pk=None):
        """
        GET  /api/books/{id}/reviews/ — получить рецензии книги
        POST /api/books/{id}/reviews/ — оставить рецензию
        """
        book = self.get_object()  # Получаем книгу по pk из URL

        if request.method == 'GET':
            reviews = book.reviews.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            # Проверяем авторизацию
            if not request.user.is_authenticated:
                return Response(
                    {'detail': 'Необходима авторизация'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            serializer = ReviewSerializer(
                data=request.data,
                context={'request': request}  
            )
            if serializer.is_valid():
                serializer.save(book=book)  # Передаём book автоматически
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            # serializer.errors — словарь с ошибками валидации
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='top-rated')
    def top_rated(self, request):
        """
        GET /api/books/top-rated/ — книги с наивысшим рейтингом.
        """
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
