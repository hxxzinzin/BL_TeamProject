from django.shortcuts import render
from .models import Store
from .serializers import StoreSerializer
from rest_framework.viewsets import ModelViewSet

class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer