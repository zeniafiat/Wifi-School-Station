from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

# Create your views here.
from main.models import DATT
from users.models import UserProfile
from django.contrib.auth.models import User
from .serializers import DATTSerializer
from .serializers import RegisterSerializer


class   DATTAPIVIEVSET(viewsets.ModelViewSet):
    queryset = DATT.objects.all()
    serializer_class = DATTSerializer

class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Пользователь успешно зарегистрирован.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckUserExists(APIView):
    #http://localhost:8000/api/check-user/?username=ivan&password=123456
    def get(self, request):
        username = request.query_params.get('username')
        password = request.query_params.get('password')

        if not username:
            return Response({'error': 'Username не указан'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            exists = True
            password_match = check_password(password, user.password)
            return Response({
                'exists': exists,
                'password_match': password_match
            })
        except User.DoesNotExist:
            return Response({'exists': False})


class UpdateTelegramIDView(APIView):
    def put(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        telegram_id = request.data.get('telegram_id')

        if not all([username, password, telegram_id]):
            return Response(
                {'error': 'Все поля (username, password, telegram_id) обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )
        print(username, password)
        # Проверяем логин/пароль
        user = authenticate(username=username, password=password)
        if not user:
            print("учётные данные")
            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            # Создаем профиль, если его нет
            profile = UserProfile.objects.create(user=user)

        # Обновляем telegram_id
        profile.telegram_id = telegram_id
        profile.save()

        return Response({
            'message': 'Telegram ID успешно обновлён',
            'telegram_id': profile.telegram_id
        }, status=status.HTTP_200_OK)


class UpdateAddrView(APIView):
    def put(self, request, *args, **kwargs):
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        addr = request.data.get('addr')
        print("UpdateAddrView:",addr)

        if not all([username, password, addr]):
            return Response(
                {'error': 'Все поля (username, password, addr) обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, что addr — число
        try:
            addr = int(addr)
        except (TypeError, ValueError):
            return Response(
                {'error': 'Поле addr должно быть целым числом'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем логин/пароль
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Профиль пользователя не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Обновляем addr
        profile.sensor_id = addr
        profile.save()

        return Response({
            'message': 'Поле addr успешно обновлено',
            'addr': profile.sensor_id
        }, status=status.HTTP_200_OK)

class GetUserProfile(APIView):
    def get(self, request):
        telegram_id = request.query_params.get('telegram_id')
        if not telegram_id:
            return Response({'error': 'telegram_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            profile = UserProfile.objects.get(telegram_id=telegram_id)
            return Response({
                'sensor_id': profile.sensor_id,
                'username': profile.user.username
            })
        except UserProfile.DoesNotExist:
            return Response({'error': 'Профиль не найден'}, status=status.HTTP_404_NOT_FOUND)

class GetSensorData(APIView):
    def get(self, request):
        sensor_id = request.query_params.get('sensor_id')
        if not sensor_id:
            return Response({'error': 'sensor_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data = DATT.objects.filter(addr=sensor_id).latest('id')
            return Response(DATTSerializer(data).data)
        except DATT.DoesNotExist:
            return Response({'error': 'Данные не найдены'}, status=status.HTTP_404_NOT_FOUND)

class GetPastSensorData(APIView):
    def get(self, request):
        sensor_id = request.query_params.get('sensor_id')
        if not sensor_id:
            return Response({'error': 'sensor_id обязателен'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = DATT.objects.filter(addr=sensor_id).order_by('-id')[:10]
        return Response(DATTSerializer(data, many=True).data)