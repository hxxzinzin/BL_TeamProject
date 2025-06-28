from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Store
from .serializers import StoreSerializer
from .serializers import StoreCongestionSerializer
from rest_framework.viewsets import ModelViewSet

class StoreViewSet(ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    # 카테고리별 필터링(쿼리스트링 이용)
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

        # 여유로운순 정렬을 위한 인구 비율 계산
        # .annotate(): 기존 Store 객체들 각각에 새 필드(population_ratio)를 붙이는 역할
        queryset = queryset.annotate(
            # annotate 안은 Django ORM의 SQL 연산 표현식 공간 -> if문 못 씀 -> Case, When 사용
            population_ratio = Case(
                # 만약 0 나눗셈 방지용 -> 최대 수용 인원이 0일 때 혼잡도 최대(1.0)으로 둠
                When(max_customers = 0, then = Value(1.0)),
                # F(): 모델 필드를 참조하는 객체, * 1.0은 정수 나눗셈 방지용
                default = F('current_customers') * 1.0 / F('max_customers')
            )
        )

        return queryset
    
    # 필터(filters.~ 따로 선언하면 덮어씌워짐)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['rating', 'population_ratio']
    