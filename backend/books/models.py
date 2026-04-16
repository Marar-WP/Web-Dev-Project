from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,          
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Слаг (URL)'
    )
    description = models.TextField(
        blank=True,          
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']   

    def __str__(self):
        # __str__ — что показывать при print(category)
        return self.name


class Author(models.Model):

    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')

    # ImageField — поле для загрузки изображений
    # upload_to — куда сохранять (media/authors/)
    # null=True  — можно хранить NULL в базе данных
    # blank=True — необязательно при заполнении формы
    photo = models.ImageField(
        upload_to='authors/',
        null=True,
        blank=True,
        verbose_name='Фото'
    )

    bio = models.TextField(blank=True, verbose_name='Биография')

    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):

    title = models.CharField(max_length=300, verbose_name='Название')

    # ForeignKey — "много-к-одному"
    # Много книг принадлежат одной категории
    # on_delete=CASCADE — при удалении категории удаляются все её книги
    # on_delete=SET_NULL — при удалении категории ставит NULL (нужно null=True)
    # on_delete=PROTECT — запрещает удалять категорию, пока есть книги
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',   
        verbose_name='Категория'
    )

    authors = models.ManyToManyField(
        Author,
        related_name='books',  
        verbose_name='Авторы'
    )

    description = models.TextField(blank=True, verbose_name='Описание')
    isbn = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='ISBN')
    published_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Год издания',
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(2100),
        ]
    )
    pages = models.IntegerField(null=True, blank=True, verbose_name='Количество страниц')

    cover = models.ImageField(
        upload_to='covers/',
        null=True,
        blank=True,
        verbose_name='Обложка'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']  

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        """Вычисляет средний рейтинг книги по всем рецензиям."""
        reviews = self.reviews.all()
        if not reviews:
            return None
        total = sum(r.rating for r in reviews)
        return round(total / len(reviews), 1)

    @property
    def reviews_count(self):
        return self.reviews.count()


class Review(models.Model):

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,   
        related_name='reviews',     
        verbose_name='Книга'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',      
        verbose_name='Пользователь'
    )

    # IntegerField с валидаторами — рейтинг от 1 до 5
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Минимальный рейтинг: 1'),
            MaxValueValidator(5, message='Максимальный рейтинг: 5'),
        ],
        verbose_name='Рейтинг'
    )

    text = models.TextField(verbose_name='Текст рецензии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
        ordering = ['-created_at']
        unique_together = ['book', 'user']

    def __str__(self):
        return f'Рецензия {self.user.username} на "{self.book.title}"'
