from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from main.models import DATT
from .serializers import DATTSerializer


class   DATTAPIVIEVSET(viewsets.ModelViewSet):
    queryset = DATT.objects.all()
    serializer_class = DATTSerializer
