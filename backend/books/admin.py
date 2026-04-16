from django.contrib import admin
from .models import Category, Author, Book, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'birth_date']
    search_fields = ['first_name', 'last_name']
    list_filter = ['birth_date']


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0       # Не показывать пустые формы для добавления
    readonly_fields = ['user', 'created_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published_year', 'reviews_count', 'average_rating']
    list_filter = ['category', 'published_year']
    search_fields = ['title', 'isbn', 'authors__last_name']
    filter_horizontal = ['authors']   # Удобный виджет для ManyToMany
    inlines = [ReviewInline]          # Показываем рецензии на странице книги

    def reviews_count(self, obj):
        return obj.reviews.count()
    reviews_count.short_description = 'Рецензий'

    def average_rating(self, obj):
        return obj.average_rating
    average_rating.short_description = 'Рейтинг'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__username']
    readonly_fields = ['created_at']
