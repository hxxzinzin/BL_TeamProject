from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Store
from .serializers import StoreSerializer
from .serializers import StoreCongestionSerializer
from rest_framework.viewsets import ModelViewSet
from django.db.models import F, Case, When, Value
from rest_framework import filters

# api view를 통해 혼잡도 입력부분 구현
### 현재 손님 수만 입력하면 알아서 혼잡도의 정도를 정해서 db에 해당 내용 저장
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_store_congestion(request, store_id):
    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response({'error': '가게를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    # 현재 손님 수를 필수 입력 필드로 지정 -> 입력 안하면 err 생성
    current_customers = request.data.get('current_customers')
    if current_customers is None:
        return Response({'error': 'current_customers 값이 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 현재 손님 수가 정수형이 아니라면 에러 생성
    try:
        current_customers = int(current_customers)
    except ValueError:
        return Response({'error': 'current_customers는 정수여야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 최대 손님 수가 입력 안되어있다면 에러 생성
        # 근데 이건 우리가 직접 db에 입력하는거라면 굳이 싶긴한데 그래도 넣는게 안전할 듯
    max_customers = store.max_customers
    if max_customers <= 0:
        return Response({'error': 'max_customers 값이 설정되어 있지 않거나 0입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 현재 인원수가 최대 수용 인원보다 크다면 에러 생성
    if current_customers > max_customers:
        return Response({'error': 'current_customers가 max_customers보다 클 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)


    # 혼잡도 계산
    ratio = current_customers / store.max_customers
    if ratio < 0.25:
        congestion = 'low'
    elif ratio < 0.75:
        congestion = 'medium'
    else:
        congestion = 'high'

    # serializer 입력용의 데이터 딕셔너리 구성
    data = {
        'current_customers': current_customers,
        'congestion': congestion
    }

    serializer = StoreCongestionSerializer(store, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 가게 혼잡도 정보 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_store_congestion(request, store_id):
    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response({'error': '가게를 찾을 수 없습니다.'}, status=404)

    serializer = StoreSerializer(store)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
    