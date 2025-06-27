from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.ModelSerializer): 
    # 현재 시간에 따라 값이 입력되는 is_open, is_breaktime 필드
    # SerializerMethodField(): 읽기 전용 필드, 직렬화 시에 동적으로 계산된 값을 넣고 싶을 때 사용
    is_open = serializers.SerializerMethodField()
    is_breaktime = serializers.SerializerMethodField()

    # 필드 선언하면 직렬화 할 때 이 메소드를 자동으로 호출
    # 이름 규칙: get_필드명
    def get_is_open(self, obj):
        return obj.is_open_now()

    def get_is_breaktime(self, obj):
        return obj.is_breaktime_now()

    class Meta:
        model = Store
        fields = [ 'id', 'category', 'subcategory', 'photo', 'name', 
                  'rating', 'address', 'latitude', 'longitude', 
                  'congestion', 'current_customers', 'max_customers', 
                  'open_time', 'close_time', 'break_start_time', 'break_end_time', 
                  'is_open', 'is_breaktime', 'naver_url', 'created_at' ]
        # is_open, is_breaktime은 모델에는 필요 없는 필드지만, 프론트에는 보내줘야 함

