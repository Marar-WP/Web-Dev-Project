from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'', views.BookViewSet, basename='book')
router.register(r'reviews', views.ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),

    # =========================
    # FBV (Function-Based Views)
    # =========================
    path('fbv/top-rated/', views.top_rated_books_fbv),
    path('fbv/<int:book_id>/reviews/', views.book_reviews_fbv),

    # =========================
    # CBV (APIView)
    # =========================
    path('cbv/categories/', views.CategoryListCreateAPIView.as_view()),
    path('cbv/authors/', views.AuthorListCreateAPIView.as_view()),
]