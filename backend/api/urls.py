from django.urls import path
from api.views import (
    ProductListAPIView,
    ProductDetailAPIView,
    CategoryListAPIView,
    CategoryDetailAPIView,
)

urlpatterns = [
    path('books/', ProductListAPIView.as_view()),
    path('books/<int:product_id>/',ProductDetailAPIView.as_view()),
    path('categories/',CategoryListAPIView.as_view()),
    path('categories/<int:category_id>/',CategoryDetailAPIView.as_view()),
]