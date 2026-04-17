"""
=============================================================
  АУТЕНТИФИКАЦИЯ ПОЛЬЗОВАТЕЛЕЙ — users/views.py
=============================================================

Здесь реализуем:
  POST /api/users/register/  — регистрация
  POST /api/users/login/     — вход
  POST /api/users/logout/    — выход
  GET  /api/users/me/        — профиль текущего пользователя
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserRegistrationSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):

    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Автоматически логиним после регистрации
        login(request, user)
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'detail': 'Укажите имя пользователя и пароль'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)  # Создаём сессию
        return Response(UserSerializer(user).data)
    else:
        return Response(
            {'detail': 'Неверное имя пользователя или пароль'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response({'detail': 'Вы успешно вышли из системы'})

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def me_view(request):

    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
