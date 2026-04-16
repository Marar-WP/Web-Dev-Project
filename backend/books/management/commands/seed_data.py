"""
=============================================================
  КАСТОМНАЯ КОМАНДА — books/management/commands/seed_data.py
=============================================================

Кастомные команды manage.py позволяют создавать свои утилиты.
Запуск: python manage.py seed_data

Эта команда заполняет базу тестовыми данными.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Category, Author, Book, Review


class Command(BaseCommand):
    # Описание команды (показывается при python manage.py help)
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        """handle() — главный метод команды. Здесь пишем логику."""

        self.stdout.write('Создаю тестовые данные...')

        # --- КАТЕГОРИИ ---
        categories_data = [
            {'name': 'Фантастика', 'slug': 'fantasy', 'description': 'Научная фантастика и фэнтези'},
            {'name': 'Классика', 'slug': 'classic', 'description': 'Классическая литература'},
            {'name': 'Детектив', 'slug': 'detective', 'description': 'Детективы и триллеры'},
            {'name': 'История', 'slug': 'history', 'description': 'Историческая литература'},
        ]

        categories = {}
        for data in categories_data:
            # get_or_create — получает объект или создаёт если не существует
            # Возвращает: (объект, был_ли_создан)
            category, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults=data  # defaults — поля при СОЗДАНИИ (не при поиске)
            )
            categories[data['slug']] = category
            if created:
                self.stdout.write(f'  ✓ Категория: {category.name}')

        # --- АВТОРЫ ---
        authors_data = [
            {'first_name': 'Фрэнк', 'last_name': 'Герберт', 'bio': 'Американский писатель-фантаст, автор "Дюны"'},
            {'first_name': 'Лев', 'last_name': 'Толстой', 'bio': 'Великий русский писатель'},
            {'first_name': 'Агата', 'last_name': 'Кристи', 'bio': 'Королева детектива'},
            {'first_name': 'Михаил', 'last_name': 'Булгаков', 'bio': 'Русский писатель, автор "Мастера и Маргариты"'},
        ]

        authors = {}
        for data in authors_data:
            author, created = Author.objects.get_or_create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                defaults=data
            )
            authors[data['last_name']] = author
            if created:
                self.stdout.write(f'  ✓ Автор: {author.full_name}')

        # --- КНИГИ ---
        books_data = [
            {
                'title': 'Дюна',
                'description': 'Эпическая сага о пустынной планете Арракис.',
                'published_year': 1965,
                'pages': 688,
                'category': categories['fantasy'],
                'author_keys': ['Герберт'],
            },
            {
                'title': 'Война и мир',
                'description': 'Роман-эпопея о войне 1812 года.',
                'published_year': 1869,
                'pages': 1274,
                'category': categories['classic'],
                'author_keys': ['Толстой'],
            },
            {
                'title': 'Убийство в «Восточном экспрессе»',
                'description': 'Эркюль Пуаро расследует убийство в поезде.',
                'published_year': 1934,
                'pages': 256,
                'category': categories['detective'],
                'author_keys': ['Кристи'],
            },
            {
                'title': 'Мастер и Маргарита',
                'description': 'Дьявол приходит в советскую Москву.',
                'published_year': 1967,
                'pages': 480,
                'category': categories['classic'],
                'author_keys': ['Булгаков'],
            },
        ]

        books = []
        for data in books_data:
            author_keys = data.pop('author_keys')
            book, created = Book.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            # ManyToMany поля устанавливаем отдельно через .set()
            book.authors.set([authors[key] for key in author_keys])
            books.append(book)
            if created:
                self.stdout.write(f'  ✓ Книга: {book.title}')

        # --- ПОЛЬЗОВАТЕЛИ И РЕЦЕНЗИИ ---
        users_data = [
            {'username': 'reader1', 'email': 'reader1@example.com', 'password': 'testpass123'},
            {'username': 'reader2', 'email': 'reader2@example.com', 'password': 'testpass123'},
        ]

        test_users = []
        for data in users_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={'email': data['email']}
            )
            if created:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(f'  ✓ Пользователь: {user.username} (пароль: {data["password"]})')
            test_users.append(user)

        # Добавляем рецензии
        reviews_data = [
            {'book': books[0], 'user': test_users[0], 'rating': 5, 'text': 'Шедевр! Лучшая книга в жанре фантастики.'},
            {'book': books[0], 'user': test_users[1], 'rating': 4, 'text': 'Очень глубокая книга, но читается непросто.'},
            {'book': books[1], 'user': test_users[0], 'rating': 5, 'text': 'Великий роман на все времена.'},
            {'book': books[2], 'user': test_users[1], 'rating': 5, 'text': 'Классический детектив Кристи!'},
            {'book': books[3], 'user': test_users[0], 'rating': 5, 'text': 'Рукописи не горят!'},
        ]

        for data in reviews_data:
            review, created = Review.objects.get_or_create(
                book=data['book'],
                user=data['user'],
                defaults={'rating': data['rating'], 'text': data['text']}
            )
            if created:
                self.stdout.write(f'  ✓ Рецензия на "{review.book.title}"')

        # self.style.SUCCESS — зелёный цвет в терминале
        self.stdout.write(self.style.SUCCESS('\n✅ Тестовые данные успешно добавлены!'))
        self.stdout.write(self.style.WARNING('\nТестовые аккаунты:'))
        self.stdout.write('  reader1 / testpass123')
        self.stdout.write('  reader2 / testpass123')
