from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#아이디 중복 확인 실시간 검사에 사용
@api_view(['GET'])
def check_username(request):
    username = request.query_params.get('username')

    is_taken = User.objects.filter(username=username).exists()
    return Response({'is_taken': is_taken})