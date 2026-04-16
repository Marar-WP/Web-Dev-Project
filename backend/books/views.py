"""
=============================================================
  VIEWS (ПРЕДСТАВЛЕНИЯ) — books/views.py
=============================================================

View — это обработчик HTTP-запросов.
Получает запрос → обрабатывает → возвращает ответ.

DRF предоставляет несколько уровней абстракции:

УРОВЕНЬ 1 — APIView (базовый):
  class BookView(APIView):
      def get(self, request):   ← явно пишем метод для GET
          ...
      def post(self, request):  ← и для POST
          ...

УРОВЕНЬ 2 — Generic Views (удобнее):
  class BookListView(ListCreateAPIView):
      queryset = Book.objects.all()
      serializer_class = BookSerializer
  # Django сам реализует GET (список) и POST (создание)!

УРОВЕНЬ 3 — ViewSets (максимально коротко, используем здесь):
  class BookViewSet(ModelViewSet):
      queryset = Book.objects.all()
      serializer_class = BookSerializer
  # Один класс = все CRUD операции (GET/POST/PUT/DELETE)!

HTTP МЕТОДЫ → CRUD:
  GET    /api/books/       → list()    — список книг
  POST   /api/books/       → create()  — создать книгу
  GET    /api/books/{id}/  → retrieve()— одна книга
  PUT    /api/books/{id}/  → update()  — обновить книгу
  DELETE /api/books/{id}/  → destroy() — удалить книгу
"""

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Category, Author, Book, Review
from .serializers import (
    CategorySerializer, AuthorSerializer,
    BookListSerializer, BookDetailSerializer, ReviewSerializer
)
from .permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для категорий.
    ModelViewSet даёт нам все 5 операций CRUD сразу.
    """
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


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для книг.

    Особенности:
    - Разные сериализаторы для списка и детали
    - Поиск и фильтрация
    - Кастомные действия (@action)
    """
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

        # request.query_params — это словарь параметров из URL
        # ?category=1 → request.query_params.get('category') = '1'
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
    @action(detail=True, methods=['get', 'post'], url_path='reviews')
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
                context={'request': request}  # Передаём request для получения user
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
        # Получаем все книги с рецензиями и считаем средний рейтинг в Python
        books = self.get_queryset()
        rated_books = [(book, book.average_rating) for book in books if book.average_rating]
        rated_books.sort(key=lambda x: x[1], reverse=True)
        top_books = [book for book, _ in rated_books[:10]]

        serializer = BookListSerializer(top_books, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для рецензий.

    Пользователь может только свои рецензии редактировать/удалять.
    Использует кастомный permission class.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.select_related('user', 'book').all()

    def perform_create(self, serializer):
        """
        perform_create вызывается при создании объекта.
        Автоматически ставим текущего пользователя.

        perform_create(serializer) → serializer.save(**kwargs)
        """
        serializer.save(user=self.request.user)
