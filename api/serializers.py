from rest_framework import serializers
from main.models import DATT
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class DATTSerializer(serializers.ModelSerializer):
    class Meta:
        model = DATT
        fields = "__all__"



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user