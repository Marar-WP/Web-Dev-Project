 # ПРАВА ДОСТУПА — books/permissions.py

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем: текущий пользователь = автор объекта?
        return obj.user == request.user
