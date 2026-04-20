from django.urls import path
from .views.cbv import BookListAPIView, BookDetailAPIView
from .views.fbv import book_list_fbv, book_detail_fbv, category_list_fbv

urlpatterns = [
    # CBV — APIView
    path('cbv/books/', BookListAPIView.as_view(), name='cbv-book-list'),
    path('cbv/books/<int:pk>/', BookDetailAPIView.as_view(), name='cbv-book-detail'),

    # FBV — @api_view
    path('fbv/books/', book_list_fbv, name='fbv-book-list'),
    path('fbv/books/<int:pk>/', book_detail_fbv, name='fbv-book-detail'),
    path('fbv/categories/', category_list_fbv, name='fbv-category-list'),
]
