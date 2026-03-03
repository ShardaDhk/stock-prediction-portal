from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User #in built django model, not custom model
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.routers import Response


class ResgisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = {
            'status': 'Request was permitted'
        }
        return Response(response)
