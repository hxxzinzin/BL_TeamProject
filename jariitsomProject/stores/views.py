from django.shortcuts import render
from .models import Store
from .serializers import StoreSerializer
from rest_framework.viewsets import ModelViewSet

class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_queryset(self):
        queryset = Store.objects.all() # 여기에 한 번 더 선언 해줘야 됨
        category = self.request.query_params.get('category')
        subcategory = self.request.query_params.get('subcategory')

        if category is not None:
            queryset = queryset.filter(category=category)
            # 왼쪽 카테고리는 필드 이름(인자명), 오른쪽 카테고리는 쿼리스트링에서 받아온 값(변수)
            # 변수명 헷갈리면 바꾸기
        if subcategory is not None:
            queryset = queryset.filter(subcategory=subcategory)
            # 조건이 대체 되는 게 아닌 누적 되는 식으로 작동함

        return queryset