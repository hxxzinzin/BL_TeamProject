from django.db import models

class Store(models.Model) : 
    #리스트[] & 튜플(), choices는 튜플 또는 튜플 리스트만 허용
    CATEGORY_CHOICES = [
        #'DB에 저장될 값', '사용자에게 보여줄 이름'
        ('restaurant', '음식점'),
        ('cafe', '카페/디저트'),
    ]
    SUBCATEGORY_CHOICES = [
        ('korean', '한식'),
        ('snack', '분식'),
        ('japanese', '일식'),
        ('fastfood', '패스트푸드'),
        ('salad', '샐러드'),
    ]

    CONGESTION_CHOICES = [
        ('low', '여유'),
        ('medium', '보통'),
        ('high', '혼잡'),
    ]

    #필터링을 위한 카테고리
    category = models.CharField(verbose_name="카테고리", max_length=20, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(verbose_name="음식 종류", max_length=20, choices=SUBCATEGORY_CHOICES, blank=True, null=True)
    
    photo = models.ImageField(verbose_name="가게 이미지", 
                              blank=True, null=True, upload_to='store_photo')
    name = models.CharField(verbose_name="가게 이름", max_length=100)
    rating = models.FloatField(verbose_name="별점", default=0.0)
    
    #위치, 거리
    address = models.CharField(verbose_name="주소", max_length=200)
    latitude = models.FloatField(verbose_name="위도")
    longitude = models.FloatField(verbose_name="경도")
    
    #혼잡도
    congestion = models.CharField(verbose_name="혼잡도", max_length=10, choices=CONGESTION_CHOICES, default='low')
    current_customers = models.IntegerField(verbose_name="현재 손님 수", default=0)
    max_customers = models.IntegerField(verbose_name="최대 수용 인원", default=0)

    #가게 정보
    is_open = models.BooleanField(verbose_name="영업 여부", default=True)
    is_breaktime = models.BooleanField(verbose_name="브레이크 타임 여부", default=False)

    naver_url = models.URLField(verbose_name="가게 네이버 링크", blank=True, null=True)

    created_at = models.DateTimeField(verbose_name="등록일", auto_now_add=True)
    
    def __str__(self):
        return self.name