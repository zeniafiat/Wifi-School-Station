from rest_framework import serializers
from main.models import DATT


class DATTSerializer(serializers.ModelSerializer):
    class Meta:
        model = DATT
        fields = "__all__"