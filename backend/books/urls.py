"""
=============================================================
  URL-МАРШРУТЫ — books/urls.py
=============================================================

Router автоматически создаёт URL-маршруты из ViewSet.

Один ViewSet → Router создаёт:
  /api/books/             GET  → list()
  /api/books/             POST → create()
  /api/books/{id}/        GET  → retrieve()
  /api/books/{id}/        PUT  → update()
  /api/books/{id}/        PATCH → partial_update()
  /api/books/{id}/        DELETE → destroy()

Плюс наши кастомные @action:
  /api/books/{id}/reviews/  GET/POST → reviews()
  /api/books/top-rated/     GET      → top_rated()
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаём роутер
router = DefaultRouter()

# Регистрируем ViewSets в роутере
# router.register(prefix, viewset, basename)
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'', views.BookViewSet, basename='book')         # /api/books/
router.register(r'reviews', views.ReviewViewSet, basename='review')

# router.urls — список всех URL, которые сгенерировал роутер
urlpatterns = [
    path('', include(router.urls)),
]
