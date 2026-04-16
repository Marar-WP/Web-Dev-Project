# 📚 Book Library — Django REST API

Бэкенд для приложения "Библиотека книг" на Django + Django REST Framework.

---

## 🗂 Структура проекта

```
book_library/
├── config/                  ← Настройки проекта
│   ├── settings.py          ← Главный конфиг (БД, приложения, CORS...)
│   ├── urls.py              ← Главные URL-маршруты
│   └── wsgi.py              ← Точка входа для production
│
├── books/                   ← Приложение "Книги"
│   ├── models.py            ← Модели: Category, Author, Book, Review
│   ├── serializers.py       ← JSON ↔ Python объекты
│   ├── views.py             ← Обработчики запросов (ViewSets)
│   ├── urls.py              ← URL маршруты книг
│   ├── admin.py             ← Панель администратора
│   ├── permissions.py       ← Правила доступа
│   └── management/
│       └── commands/
│           └── seed_data.py ← Команда: заполнить тестовыми данными
│
├── users/                   ← Приложение "Пользователи"
│   ├── views.py             ← register, login, logout, me
│   ├── serializers.py       ← UserSerializer
│   └── urls.py              ← URL маршруты пользователей
│
├── manage.py                ← Утилита управления Django
├── requirements.txt         ← Зависимости
└── README.md                ← Этот файл
```

---

## 🚀 Быстрый старт

### 1. Создай виртуальное окружение
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 2. Установи зависимости
```bash
pip install -r requirements.txt
```

### 3. Создай таблицы в базе данных
```bash
# makemigrations — создаёт файлы миграций из моделей
python manage.py makemigrations books users

# migrate — применяет миграции (создаёт таблицы в БД)
python manage.py migrate
```

### 4. Создай суперпользователя (для /admin/)
```bash
python manage.py createsuperuser
```

### 5. Заполни тестовыми данными
```bash
python manage.py seed_data
```

### 6. Запусти сервер
```bash
python manage.py runserver
```

Сервер запустится на http://localhost:8000

---

## 🔗 API Эндпоинты

### Пользователи
| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/users/register/` | Регистрация |
| POST | `/api/users/login/` | Вход |
| POST | `/api/users/logout/` | Выход |
| GET/PUT | `/api/users/me/` | Свой профиль |

### Книги
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/books/` | Список книг |
| POST | `/api/books/` | Создать книгу |
| GET | `/api/books/{id}/` | Детали книги |
| PUT | `/api/books/{id}/` | Обновить книгу |
| DELETE | `/api/books/{id}/` | Удалить книгу |
| GET/POST | `/api/books/{id}/reviews/` | Рецензии книги |
| GET | `/api/books/top-rated/` | Топ по рейтингу |

### Авторы
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/books/authors/` | Список авторов |
| GET | `/api/books/authors/{id}/` | Детали автора |

### Категории
| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/books/categories/` | Список категорий |
| GET | `/api/books/categories/{id}/` | Детали категории |

---

## 🔍 Фильтрация и поиск

```
# Поиск по названию/автору
GET /api/books/?search=дюна

# Фильтр по категории
GET /api/books/?category=1

# Фильтр по автору
GET /api/books/?author=1

# Сортировка
GET /api/books/?ordering=published_year
GET /api/books/?ordering=-created_at   (минус = убывание)

# Пагинация (10 книг на страницу)
GET /api/books/?page=2
```

---

## 📝 Примеры запросов (для тестирования)

### Регистрация
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alex","email":"alex@test.com","password":"pass1234","password2":"pass1234"}'
```

### Список книг
```bash
curl http://localhost:8000/api/books/
```

### Оставить рецензию (нужна авторизация)
```bash
curl -X POST http://localhost:8000/api/books/1/reviews/ \
  -H "Content-Type: application/json" \
  -u reader1:testpass123 \
  -d '{"rating":5,"text":"Отличная книга!"}'
```

---

## 🔑 Ключевые концепции Django (учись здесь!)

### Модели → Таблицы БД
Каждый класс в `models.py` = таблица. Django создаёт SQL автоматически.

### ORM — работа с БД без SQL
```python
# В Django shell (python manage.py shell):
from books.models import Book

Book.objects.all()              # Все книги
Book.objects.filter(year=1965)  # Фильтр
Book.objects.get(id=1)          # Один объект
Book.objects.create(title="...") # Создать
book.save()                      # Сохранить
book.delete()                    # Удалить
```

### Миграции — контроль версий БД
```bash
# Изменил модель → создай миграцию
python manage.py makemigrations

# Применить все миграции
python manage.py migrate

# Посмотреть SQL миграции
python manage.py sqlmigrate books 0001
```

### DRF Браузерный интерфейс
Открой http://localhost:8000/api/books/ в браузере —
DRF покажет красивый интерфейс для тестирования API!

---

## 🔧 Подключение к Angular

В Angular используй `HttpClient` и настрой прокси:

```typescript
// environment.ts
export const environment = {
  apiUrl: 'http://localhost:8000/api'
};
```

```typescript
// book.service.ts
getBooks(): Observable<Book[]> {
  return this.http.get<Book[]>(`${environment.apiUrl}/books/`);
}
```

