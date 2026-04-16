"""
URL-маршрутизация в Django работает так:
  1. Приходит запрос: GET /api/books/
  2. Django смотрит в этот файл
  3. Находит совпадение: path('api/books/', ...)
  4. Передаёт запрос нужному View (обработчику)

include() позволяет "подключать" URL-файлы из других приложений.
Это делает код модульным и чистым.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/books/', include('books.urls')),      # /api/books/...
    path('api/users/', include('users.urls')),      # /api/users/...

    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
